#!/usr/bin/python

#----------------------------------------------------------------------
# Autor:          Petr Pouč                                           
# Login:          xpoucp01
# Datum:          06.01.2022
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




bacons_table = ["00000", "00001", "00010", "00011", "00100", "00101", "00110", "00111", "01000",
               "01001", "01010", "01011", "01100", "01101", "01110", "01111", "10000", "10001", "10010",
               "10011", "10100", "10101", "10110", "10111"]

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "(I,J)", "K", "L", "M", "N", "O", "P","Q",
            "R", "S", "T", "(U/V)", "W", "X", "Y", "Z"]


class SplitDocument:
   doc_ref = ""
   paragraphs = []
   secret_message = ""

def updateZip(zipname, zip_file_location, outside_file_location):
   # generate a temp file
   tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
   os.close(tmpfd)

   # create a temp copy of the archive without filename            
   with zipfile.ZipFile(zipname, 'r') as zin:
      with zipfile.ZipFile(tmpname, 'w') as zout:
         zout.comment = zin.comment # preserve the comment
         for item in zin.infolist():
               print(item.filename, item.filename != zip_file_location, item.filename)
               if item.filename != zip_file_location:
                  zout.writestr(item, zin.read(item.filename))

   # replace with the temp archive
   os.remove(zipname)
   os.rename(tmpname, zipname)

   # now add filename with its new data
   with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
      zf.write(outside_file_location, zip_file_location)

# returns <w:rStyle w:val="boldstyle"/>
def create_boldstyle_el():
   namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
   tag = namespace + 'rStyle'
   ns_val = namespace + 'val'
   el = xml.etree.ElementTree.Element(tag)
   el.attrib[ns_val] = "boldstyle"
   return el

# todo zkontrolovat mezery
def split_to_words(string):
   word = string.strip().split()
   return(word)
   # return [word for word in string.strip().split() if not word == '' and not word == ' ' ]

def new_run_element(word, bit, properties_to_inherit):
   namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
   run_tag = namespace + 'r'
   run_properties = namespace + 'rPr'
   text_tag = namespace + 't'


   new_run = xml.etree.ElementTree.Element(run_tag)
   if properties_to_inherit is None:
      prop_el = xml.etree.ElementTree.Element(run_properties)
   else:
      prop_el = deepcopy(properties_to_inherit)


   #bit který je nutno zašifrovat
   if bit == "1":
      # apply <w:rStyle w:val="boldstyle"/>  
      for subelement in prop_el[:]:
         # print(subelement.tag)
         
         #namespaces které musím odstranit, kvůli kolizím s mým vlastním stylem
         if(subelement.tag == namespace + "rFonts"):
            prop_el.remove(subelement)
         elif(subelement.tag == namespace + "szC"):
            prop_el.remove(subelement)
         elif(subelement.tag == namespace + "sz"):
            prop_el.remove(subelement)
      style_el = create_boldstyle_el()
      prop_el.append(style_el)
   
   new_run.append(prop_el)

   text_el = xml.etree.ElementTree.Element(text_tag)
   text_el.text = word
   text_el.attrib["xml:space"] = "preserve"
   new_run.append(text_el)
   return new_run

#původní dokument se rozloží na odstavce,runy a slova, ty se následně s jiným stylem uloží do nového dokumentu
def split_document(message_pattern,file):
   shutil.copyfile(file, "encoded.docx")    

   new_doc = Document("encoded.docx")
   message_len = len(message_pattern)
   msg_iter = iter(message_pattern)

   font_styles = new_doc.styles
   custom_style_present = False
   for style in font_styles:
      if 'bold_style' == style.name:
         custom_style_present = True

   #nastavení custom sytlu
   if not custom_style_present:
      font_charstyle = font_styles.add_style('boldstyle', WD_STYLE_TYPE.CHARACTER)
      font_object = font_charstyle.font
      font_object.size = Pt(10)
      font_object.name = 'Arial'


   save_path = 'encoded'   
   file = file.split("/")
   file_name = 'encoded_'+file[1]


   try:
      full_path = os.path.join(save_path, file_name)
   except:
      print("Non existing path")
      sys.exit()

   new_doc.save(full_path)
 

   property_start = "<w:rPr>"
   property_end = "</w:rPr>"
   # print((doc_xml.split(property_start))[1].split(property_end)[0])

   namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
   paragraph_tag = namespace + 'p'
   run_tag = namespace + 'r'
   para_properties_tag = namespace + 'pPr'
   run_properties = namespace + 'rPr'
   text = namespace + 't'

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
         'o':"http://schemas.microsoft.com/office/drawing/2017/model3d",\
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

   # print("--")
   # print(f"{tree.tag}")

   for par in tree.iter(paragraph_tag): # todo místo iter findall (tohle asi hledá i v dětech dětí)
      new_runs = []
      # print("<w:p>")
      for run in par.findall(run_tag): #<w:p>-><w:r>
         # print("<w:r>")
         run_props_q_res = run.findall(run_properties) #<w:p>-><w:r>-><w:rPr>
         if len(run_props_q_res) == 0:
            run_props = None
         else:
            run_props = run_props_q_res[0]
         text_node = run.findall(text)[0]

         run_text = text_node.text
         # print(f"iter run: {run_text}")

         words = split_to_words(run_text)
         for word in words:
            # print("--"+word+"--")
            
            word = word + " "
            bit = next(msg_iter, None)
            new_run = new_run_element(word, bit, run_props)
            new_runs.append(new_run)

         par.remove(run)

         # print("<w:t>")
      
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

   print(full_path)
   updateZip(full_path, 'word/document.xml', "document.xml")
    

   # file = file.split("/")
   save_path = 'encoded'
   file_name = 'encoded_'+file[1]


   # try:
   #    full_path = os.path.join(save_path, file_name)
   # except:
   #    print("Non existing path")
   #    sys.exit()
   # # print(full_path)

   # new_doc.save(full_path)
   return full_path

#vytvoření docx kopie, včetně všech stylů
def copy_docx(doc):
   copy_styles = deepcopy(doc)
   return copy_styles


def listToString(s): 
    string = ""
    for ch in s: 
        string += ch  
    return string 

#převedení textového řetězce na binární podobu
def str_to_binary(message):
   binary_message = ''.join(format(ord(i), '08b') for i in message)
   print("Message is: " + message)
   return binary_message
   
def split(word):
   return [char for char in word]


#převedení binárních dat do čitelné podoby
def binary_to_str(binary):
   binary_length = len(binary)
   data = [binary[i:i+8] for i in range(0,binary_length,8)]
   integer_form = []
   character_form = ""
   for i in data:
      integer_form.append(int(i, 2))

   for i in integer_form:
      character_form = character_form + chr(i)
   return character_form

#převede vzory z cover textu do stringové podoby (tajné zprávy)
def bacon_pattern_to_string(bacons_patterns, bacons_table):
   bacons_decoded_message = ""    
   for k in range(len(bacons_patterns)):
      for l in range(len(bacons_table)):
         if(bacons_patterns[k] == bacons_table[l]):
            bacons_decoded_message = bacons_decoded_message + alphabet[l]
   return bacons_decoded_message

#cite: https://stackoverflow.com/questions/
# 17850227/text-replace-in-docx-and-save-the-changed-
# file-with-python-docx?fbclid=IwAR1UW4I7x9NqECjwN-
# 1dk2Ysy1HCagCHX-iDkKqUcmWTd1RykxF7th3LcCA
def docx_replace(old_file,new_file,rep):
   zin = zipfile.ZipFile (old_file, 'r')
   zout = zipfile.ZipFile (new_file, 'w')
   for item in zin.infolist():
      buffer = zin.read(item.filename)
      if (item.filename == 'word/document.xml'):
         res = buffer.decode("utf-8")
         for r in rep:
               res = res.replace(r,rep[r])
         buffer = res.encode("utf-8")
      zout.writestr(item, buffer)
   zout.close()
   zin.close()


def print_text(file):
   complete_text = []
   doc = docx.Document(file)
   for paragraph in doc.paragraphs:
      complete_text.append(paragraph.text)
   cover_text = '\n'.join(complete_text)
   return cover_text

#ukrytí tajné zprávy pomocí Baconovy šifry
def Bacon_encode(file, message):
       
   # docx_replace(file, "novy_file.docx", {"Lorem": "AAAAAA"})
       
   fileDir = os.path.dirname(os.path.realpath(__file__))
   filename = os.path.join(fileDir, file)

   # print(filename)

   try:
      doc = docx.Document(filename)
   except:
      print("Non existing file")
      sys.exit()

   # binary_message = str_to_binary(message)
   # print("Binary message: " + binary_message)

   message = split(message)
   message_string = listToString(message)

   index_array = []
   for i in range(len(message)):
      index_array.append(string.ascii_lowercase.index(message[i]))

 
   print(index_array)

   message_pattern = []
   for k in index_array:
      #nutné upravit hodnoty indexů, kvůli dvojicím i,j a u,v (mají stejný vzor v Baconově šifře)
      if(k > 8 and k <= 19):
         k -= 1
      elif(k == 20):
         k -= 1
      elif(k > 20):
         k -= 2
      
      message_pattern.append(bacons_table[k])

   
   pattern_string = listToString(message_pattern)
   print(message_pattern)
   print("\n", end='')

   #nutno zjistit počet slov, více slov umožňuje ukrytí delší zprávy
   full_text = print_text(file)

   word_list = full_text.split()
   number_of_words = len(re.findall(r'\w+', full_text))

   if(len(message*5) > number_of_words):
      print("Cover text doesn't have enough capacity to hide this message")
      sys.exit()
   
   
   path = split_document(pattern_string, file)
   return path

      
def Bacon_decode(file):
   try:
      doc = Document(file)
   except:
      print("Non existing file")
      sys.exit()

   font_styles = doc.styles

   bold_words = []
   non_bold = []
   binary = "" #bold = 1, nonbold = 0
   text = ""

   
   #rozdělí text na tučné a obyčejné slova
   for paragraph in doc.paragraphs:
      text = text + paragraph.text + " "

      for run in paragraph.runs:
         # #pro kódování a dekódování Baconovou šifrou nepracuji s bílými znaky (pro práci s nimi je implementována jiná metoda)
         t = run.text
         split = t.strip().split(" ")
      
         for word in split:
            if run.style.name == "boldstyle":
               bold_words.append(word)
               binary = binary + '1';
            elif run:
               if run.text != ' ':
                  non_bold.append(word)
                  binary = binary + '0';

 

   #rozdělení na vzory po 5
   bacons_patterns = re.findall('.....',binary)

   message = bacon_pattern_to_string(bacons_patterns, bacons_table)

   #binární podoba texta
   print("The binary value is:", bacons_patterns)

   # #zpráva převedena z binární podoby
   # message = binary_to_str(binary)
   return message

def Reading_txt(file):
   with open(file) as f:
      text = f.read()
   return text

class Config:
   inputfile = ''
   outputfile = ''
   decode = False
   encode = False
   message = ''
   bacon = False
   whitespaces = False
   english_replace = False

# zpracování vstupních argumentů
def ArgumentsParsing(argv):
       
   #načtení defaultních hodnot
   cfg = Config()
   try:
      opts, args = getopt.getopt(sys.argv[1:],"i:ed:s:bwr",['ifile=','encode','decode','message','bacon','whitespaces','english_replace'])
   except getopt.GetoptError:
     print("steganography.py -i <inputfile> -e/-d -s <secret_message> -<b/w/b>")
     sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
        print("test.py -i <inputfile> -o <outputfile> -e/-d")
        sys.sys.exit()
      elif opt in ('-i', '--ifile'):
         cfg.inputfile = arg
      elif opt in ('-e', '--encode'):
         cfg.encode = True
      elif opt in ('-d', '--decode'):
         cfg.decode = True
      elif opt in ('-s', '--message'):
         cfg.message = arg
      elif opt in ('-b','--bacon'):
         cfg.bacon = True
      elif opt in ('-w','--whitespaces'):
         cfg.whitespaces = True
      elif opt in ('-r','--english_replace'):
         cfg.english_replace = True
   return cfg

def main(argv):

   cfg = ArgumentsParsing(argv)
   if(cfg.bacon is False and cfg.whitespaces is False and cfg.english_replace is False):
      print("You need to use parameter --bacon/--whitespaces/--english_replace for choosing a method\nOr you can use shortcuts -b/-w/-r")
      print("\n", end='')
      sys.exit()

   print("\n", end='')
   print ("Input file: {0}" .format(cfg.inputfile))

   #vstupní cover text je docs
   if(cfg.inputfile.endswith('.docx')):
      print("\n", end='')

      #Dekódování Baconovou šifrou
      if(cfg.decode is True):
         if(cfg.bacon is True):
                secret_message = Bacon_decode(cfg.inputfile)
         elif(cfg.whitespaces is True):
            print("TODO spaces method")
            sys.exit()
         elif(cfg.english_replace is True):
            print("TODO synonym method")
            sys.exit()
         print("The secret message is:", secret_message)
         print("\n", end='')

         file_path = cfg.inputfile.replace("encoded", "decoded")

         #vytvoření a zápis do souboru 
         try:
            decoded_file = open(file_path, "w")
         except:
            print("Non existing file")
            sys.exit()
         decoded_file.write(secret_message)
         decoded_file.close()
         
      elif(cfg.encode == True):
         if(cfg.message == ''):
            print("To encode you need to use parameter -s for secret message")
            sys.exit()
   
         if(cfg.bacon is True):
               file_path = Bacon_encode(cfg.inputfile, cfg.message)
         elif(cfg.whitespaces is True):
            print("TODO spaces method")
            sys.exit()
         elif(cfg.english_replace is True):
            print("TODO synonym method")
            sys.exit()


      print(print_text(cfg.inputfile))
      

   #vstupní cover text je txt, txt soubor je nahrát a zpracován jako dokument docx
   elif(cfg.inputfile.endswith('.txt')):
      text = Reading_txt(cfg.inputfile)
      print(text)

      #převedení
      txt_to_docx = docx.Document()
      txt_to_docx.add_paragraph(text)
      
      name_docx = cfg.inputfile.split('.txt')
      txt_to_docx.save(name_docx[0]+'.docx')

      Bacon_encode(name_docx[0]+'.docx', cfg.message)


   # uložení tajné zprávy do souboru: {path}, zakódované zprávy jsou uložené ve složce encoded, dekódované ve složce decoded
   print ("Output file: {0}" .format(file_path))

if __name__ == "__main__":
   main(sys.argv[1:])
     

