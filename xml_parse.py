#----------------------------------------------------------------------
# Autor:          Petr Pouč                                           
# Login:          xpoucp01
# Datum:          27.04.2022
# Název práce:    Digitální textová steganografie 
# Cíl práce:      Implementace 4 vybraných steganografických metod
#----------------------------------------------------------------------

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
from typing import List

import steganography
import bacon
import whitespaces
import synonyms


class XML_split:
   def __init__(self, message_pattern: str, file: str, method: str, bits: int) -> str:
      self.message_pattern = message_pattern
      self.file = file
      self.method = method
      self.bits = bits
   ## @brief původní dokument se rozloží na odstavce,runy a slova, ty se následně s jiným stylem uloží do nového dokumentu
   #@param message_pattern binární podoba tajné zprávy
   #@param file cesta ke cover souboru
   #@param method vybraná steganografická metoda
   #@param bits druh šifrování (pouze u metody synonym)
   #@return cesta k změněnému souboru
   def split_document(self) -> str:
         
      #pro ukončení zprávy používám counter
      cnt = 0
      shutil.copyfile(self.file, "copy.docx")    

      new_doc = Document("copy.docx")
      message_len = len(self.message_pattern)
      msg_iter = iter(self.message_pattern)

      font_styles = new_doc.styles
      
      #pro ukrytí zprávy je nejprve zapotřebí přidat vlastní styl
      if(self.method == "bacon"):
         bacon.add_bacon_style(font_styles)
         nametag = 'bacon_' 
      elif(self.method == "spaces"):
         whitespaces.add_spaces_style(font_styles)
         nametag = 'spaces_' 
      elif(self.method == "synonyms"):
         if(self.bits == "default"):
            nametag = 'synonyms_' 
         elif(self.bits == "own1"):
            nametag = 'own1_'
         elif(self.bits == "own2"):
            nametag = 'own2_'
   
      save_path = 'encoded'  
      self.file = os.path.split(self.file)
      file_name = nametag+(self.file)[1]
      
      try:
         full_path = os.path.join(save_path, file_name)
      except:
         print("Non existing path")
         sys.exit()
   
      current_dir = os. getcwd()
      isdir = os.path.isdir(current_dir + "/encoded")

      #složka encoded neexistuje
      if isdir is False:
         os.mkdir(current_dir + "/encoded") 
      
      
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
            
            run_props = None if len(run_props_q_res) == 0 else run_props_q_res[0]
               
            text_node = run.findall(text)
            if text_node:
               run_text = text_node[0].text
            else:
               par.remove(run)
               continue

            #odstranění mezer
            if(self.method == "bacon"):
               words = steganography.split_to_words(run_text)
               for word in words:
                  word = word + " "
                  bit = next(msg_iter, None)
                  new_run = new_run_element(word, bit, run_props, self.method)
                  new_runs.append(new_run)
            elif(self.method == "spaces"):
               words = re.split(r'(\s+)', run_text)
               for word in words:
                  bit = next(msg_iter, None) if word == " " else None
               
                  new_run = new_run_element(word, bit, run_props, self.method)
                  new_runs.append(new_run)
            elif(self.method == "synonyms"):
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
                  new_run = new_run_element(word, bit, run_props, self.method)
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
      if(self.method == "bacon"):
         file_name = 'bacon_'+ (self.file)[1]
      elif(self.method == "spaces"):
         file_name = 'spaces_'+ (self.file)[1]
      elif(self.method == "synonyms"):
         if(self.bits == "default"):
            file_name = 'synonyms_'+ (self.file)[1]
         elif(self.bits == "own1"):
            file_name = 'own1_'+ (self.file)[1]
         elif(self.bits == "own2"):
            file_name = 'own2_'+ (self.file)[1]

      os.remove("copy.docx")
      return full_path

#vytvoření elementů, včetně zachovaného stylu
#u slov, které nesou šifrovanou informaci mažu styl fontu a jeho velikost, neboť
#informaci ukrývám právě pomocí těhto 2 vlastností

## @brief vytvoření elementů, včetně zachovaného stylu
#@details funkce je volána v split_document() pro každé slovo původního textu
#@param word jedno slovo z celého textu
#@param bit konkrétní bit tajné zprávy
#@param properties_to_inherit zděděné XML styly (aby .docx dokument měl stejné formátování jako původní soubor)
#@param method vybraná steganografická metoda
#@return změněný run
#@pokud šifruji Baconovou šifrou,  mažu u slov které nesou šifrovanou informaci styl fontu a jeho velikost, neboť informaci ukrývám právě pomocí těhto 2 vlastností
def new_run_element(word: str, bit: int, properties_to_inherit: str, method: str) -> str:
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

   prop_el = xml.etree.ElementTree.Element(run_properties) if properties_to_inherit is None else deepcopy(properties_to_inherit)

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