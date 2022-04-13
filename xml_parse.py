from email import message
from email.errors import CharsetError
from operator import index
import sys, getopt
from xml.dom.minidom import Element
import docx
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.style import WD_STYLE_TYPE
from termcolor import colored
import numpy as np
import re
import os
import string
import shutil
import zipfile
from copy import deepcopy
import xml.etree.ElementTree as ET
from lxml import etree
from xml.etree import ElementTree
import xml.etree.ElementTree
import lxml
import xml.dom.minidom
import tempfile

import steganography
import bacon
import whitespaces
import synonyms

#původní dokument se rozloží na odstavce,runy a slova, ty se následně s jiným stylem uloží do nového dokumentu
def split_document(message_pattern,file, method, bits):
       
   #pro ukončení zprávy používám counter
   cnt = 0
   shutil.copyfile(file, "encoded.docx")    

   new_doc = Document("encoded.docx")
   message_len = len(message_pattern)
   msg_iter = iter(message_pattern)

   font_styles = new_doc.styles

   #pro ukrytí zprávy je nejprve zapotřebí přidat vlastní styl
   if(method == "bacon"):
      bacon.add_bacon_style(font_styles)
      nametag = 'bacon_' 
   elif(method == "spaces"):
      whitespaces.add_spaces_style(font_styles)
      nametag = 'spaces_' 
   elif(method == "synonyms"):
      if(bits == "default"):
         nametag = 'synonyms_' 
      elif(bits == "own1"):
         nametag = 'own1_'
      elif(bits == "own2"):
         nametag = 'own2_'
 
   save_path = 'encoded'  
   file = os.path.split(file)
   file_name = nametag+file[1]

   try:
      full_path = os.path.join(save_path, file_name)
   except:
      print("Non existing path")
      sys.exit()

   new_doc.save(full_path)

   property_start = "<w:rPr>"
   property_end = "</w:rPr>"

   namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
   paragraph_tag = namespace + 'p'
   run_tag = namespace + 'r'
   para_properties_tag = namespace + 'pPr'
   run_properties = namespace + 'rPr'
   text = namespace + 't'

   #dokument docx je nutno odzipovat
   #xml kód, který formátuji se nachází v souboru word/document.xml
   with zipfile.ZipFile(full_path) as docx:
      tree = xml.etree.ElementTree.fromstring(docx.read('word/document.xml'))

   #namespaces, které je nutné importovat v docx xml
   nms_to_reg = {
         'wpc':"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas",\
         'w14':"http://schemas.microsoft.com/office/word/2010/wordml",\
         'w':"http://schemas.openxmlformats.org/wordprocessingml/2006/main",\
         'wps':"http://schemas.microsoft.com/office/word/2010/wordprocessingShape",\
         'cx':"http://schemas.microsoft.com/office/drawing/2014/chartex",\
         'cx1':"http://schemas.microsoft.com/office/drawing/2015/9/8/chartex",\
         'cx2':"http://schemas.microsoft.com/office/drawing/2015/10/21/chartex",\
         'cx3':"http://schemas.microsoft.com/office/drawing/2016/5/9/chartex",\
         'cx4':"http://schemas.microsoft.com/office/drawing/2016/5/10/chartex",\
         'cx5':"http://schemas.microsoft.com/office/drawing/2016/5/11/chartex",\
         'cx6':"http://schemas.microsoft.com/office/drawing/2016/5/12/chartex",\
         'cx7':"http://schemas.microsoft.com/office/drawing/2016/5/13/chartex",\
         'cx8':"http://schemas.microsoft.com/office/drawing/2016/5/14/chartex",\
         'mc':"http://schemas.openxmlformats.org/markup-compatibility/2006",\
         'aink':"http://schemas.microsoft.com/office/drawing/2016/ink",\
         'am3d':"http://schemas.microsoft.com/office/drawing/2017/model3d",\
         'o':"urn:schemas-microsoft-com:office:office",\
         'r':"http://schemas.openxmlformats.org/officeDocument/2006/relationships",\
         'm':"http://schemas.openxmlformats.org/officeDocument/2006/math",\
         'v':"urn:schemas-microsoft-com:vml",\
         'wp14':"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",\
         'wp':"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",\
         'w10':"urn:schemas-microsoft-com:office:word",\
         'w15':"http://schemas.microsoft.com/office/word/2012/wordml",\
         'w16':"http://schemas.microsoft.com/office/word/2018/wordml",\
         'w16cex':"http://schemas.microsoft.com/office/word/2018/wordml/cex",\
         'w16cid':"http://schemas.microsoft.com/office/word/2016/wordml/cid",\
         'w16se':"http://schemas.microsoft.com/office/word/2015/wordml/symex",\
         'wpg':"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",\
         'wpi':"http://schemas.microsoft.com/office/word/2010/wordprocessingInk",\
         'wne':"http://schemas.microsoft.com/office/word/2006/wordml",\
         'w16sdtdh': "http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash"\
       }

   for prefix, uri in nms_to_reg.items():
      try:
         ET.register_namespace(prefix,uri)
      except:
         ET._namespace_map[uri] = prefix
   

   for par in tree.iter(paragraph_tag):
      new_runs = []
      for run in par.findall(run_tag): #<w:p>-><w:r>
         run_props_q_res = run.findall(run_properties) #<w:p>-><w:r>-><w:rPr>
         if len(run_props_q_res) == 0:
            run_props = None
         else:
            run_props = run_props_q_res[0]
            
         text_node = run.findall(text)
         if len(text_node) > 0:
            run_text = text_node[0].text
         else:
            par.remove(run)
            continue

         #odstranění mezer
         if(method == "bacon"):
            words = steganography.split_to_words(run_text)
            for word in words:
               word = word + " "
               bit = next(msg_iter, None)
               new_run = new_run_element(word, bit, run_props, method)
               new_runs.append(new_run)
         elif(method == "spaces"):
            words = re.split(r'(\s+)', run_text)
            for word in words:
               if(word == " "):
                  bit = next(msg_iter, None)
               else:
                  bit = None
              
               new_run = new_run_element(word, bit, run_props, method)
               new_runs.append(new_run)
         elif(method == "synonyms"):
            words = steganography.split_to_words(run_text)
            #kvůli ukončení dekodovani
            #todo bity pouze ke slovníkovým slovům
            for word in words:
               if cnt >= message_len:
                  break
               else:
                  if word.lower() in synonyms.dictionary_of_zeros:
                     cnt += 1 
                     bit = next(msg_iter, None)
                  elif word.lower() in synonyms.dictionary_of_synonyms:
                     cnt += 1 
                     bit = next(msg_iter, None) 
                  else:
                     bit = "x"
               new_run = new_run_element(word, bit, run_props, method)
               new_runs.append(new_run)

         par.remove(run)

      #přidání odstavců
      for new_run in new_runs:
         par.append(new_run)
      

   workaround_tree = xml.etree.ElementTree.ElementTree(tree)
   tree_root = workaround_tree.getroot()
  
   for ns, link in nms_to_reg.items():
      if ns in ["mc", "w", "w14"]:
         continue
      namespaced_ns = "xmlns:" + ns
      tree_root.attrib[namespaced_ns] = link

   #vytvoření xml s přenesenými styly + vlastní styl pro kódování zprávy
   workaround_tree.write("document.xml",encoding='UTF-8', xml_declaration=True)
   #zavření dokumentu s kterým pracujeme
   docx.close()

   # print(full_path)
   steganography.updateZip(full_path, 'word/document.xml', "document.xml")


   # file = file.split("/")
   save_path = 'encoded'
   if(method == "bacon"):
      file_name = 'bacon_'+file[1]
   elif(method == "spaces"):
      file_name = 'spaces_'+file[1]
   elif(method == "synonyms"):
      if(bits == "default"):
         file_name = 'synonyms_'+file[1]
      elif(bits == "own1"):
         file_name = 'own1_'+file[1]
      elif(bits == "own2"):
         file_name = 'own2_'+file[1]

   return full_path

#vytvoření elementů, včetně zachovaného stylu
#u slov, které nesou šifrovanou informaci mažu styl fontu a jeho velikost, neboť
#informaci ukrývám právě pomocí těhto 2 vlastností
def new_run_element(word, bit, properties_to_inherit, method):
   namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
   run_tag = namespace + 'r'
   run_properties = namespace + 'rPr'
   text_tag = namespace + 't'

   #potřebuji pro metodu synonym
   text_el = xml.etree.ElementTree.Element(text_tag)
   text_el.text = word

   keys = []
   syn = word
   for key in synonyms.dictionary_of_synonyms:
      keys.append(key)
   

   new_run = xml.etree.ElementTree.Element(run_tag)

   if properties_to_inherit is None:
      prop_el = xml.etree.ElementTree.Element(run_properties)
   else:
      prop_el = deepcopy(properties_to_inherit)


   #přidání stylů do xml souboru docx, odstranění původních (těch, které způsobují kolizi)
   if(method == "bacon"):
      bacon.bacon_element(prop_el, bit, namespace)
   elif(method == "spaces"):
      whitespaces.spaces_element(prop_el,bit,namespace)
   elif(method == "synonyms"):
      syn = synonyms.syn_element(prop_el, bit,namespace, word, new_run)
   

   text_el.text = syn
   new_run.append(prop_el)
   

   text_el.attrib["xml:space"] = "preserve"

   if method == "synonyms":
      text_el.text += " "
   new_run.append(text_el)
   return new_run