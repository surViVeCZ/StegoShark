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
import xml_parse

bacons_table = ["00000", "00001", "00010", "00011", "00100", "00101", "00110", "00111", "01000",
               "01001", "01010", "01011", "01100", "01101", "01110", "01111", "10000", "10001", "10010",
               "10011", "10100", "10101", "10110", "10111", "11111"]

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "(I,J)", "K", "L", "M", "N", "O", "P","Q",
            "R", "S", "T", "(U/V)", "W", "X", "Y", "Z", "."]


#ukrytí tajné zprávy pomocí Baconovy šifry
def Bacon_encode(file, message):
   try:
      doc = docx.Document(file)
   except:
      print("Non existing file")
      sys.exit()
   message = steganography.split(message)
   # message_string = steganography.listToString(message)

   index_array = []
   for i in range(len(message)):
      try:
         index_array.append(string.ascii_lowercase.index(message[i]))
      except:
         index_array.append(alphabet.index(message[i])+2)
 

   message_pattern = []
   print(index_array)
   for k in index_array:
      #nutné upravit hodnoty indexů, kvůli dvojicím i,j a u,v (mají stejný vzor v Baconově šifře)
      if(k > 8 and k <= 20):
         k -= 1
      elif(k > 20):
         k -= 2
      message_pattern.append(bacons_table[k])

   pattern_string = steganography.listToString(message_pattern)
   print(message_pattern)
   print("\n", end='')

   #nutno zjistit počet slov, více slov umožňuje ukrytí delší zprávy
   full_text = steganography.print_text(file)

   word_list = full_text.split()
   number_of_words = len(re.findall(r'\w+', full_text))

   #pro ukrytí jednoho znaku je potřeba 5 znaků cover textu
   if(len(message*5) > number_of_words):
      print("Cover text doesn't have enough capacity to hide this message")
      return False
   
   path = xml_parse.split_document(pattern_string, file, "bacon", "default")
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
   end_of_message = 0
   #rozdělí text na tučné a obyčejné slova
   for paragraph in doc.paragraphs:
      text = text + paragraph.text + " "

      for run in paragraph.runs:
         #ukončení zprávy
         if(end_of_message == 5):
            break
         # #pro kódování a dekódování Baconovou šifrou nepracuji s bílými znaky (pro práci s nimi je implementována jiná metoda)
         t = run.text
         split = t.strip().split(" ")
      
         for word in split:
            if run.style.name == "baconstyle":
               bold_words.append(word)
               binary += '1';
               end_of_message += 1
            elif run:
               if run.text != ' ':
                  non_bold.append(word)
                  binary += '0';
                  end_of_message = 0
           


   #rozdělení na vzory po 5
   bacons_patterns = re.findall('.....',binary)
   message = bacon_pattern_to_string(bacons_patterns, bacons_table)

   #binární podoba texta
   # print("The binary value is:", bacons_patterns)

   # #zpráva převedena z binární podoby
   # message = binary_to_str(binary)
   return message

   #převede vzory z cover textu do stringové podoby (tajné zprávy)
def bacon_pattern_to_string(bacons_patterns, bacons_table):
   bacons_decoded_message = ""
   for k in range(len(bacons_patterns)):
      for l in range(len(bacons_table)):
         #11111 je ukončovací znak, zprávu ukončujeme "."
         if(bacons_patterns[k] == bacons_table[l]):
            bacons_decoded_message += alphabet[l]
   return bacons_decoded_message

# returns <w:rStyle w:val="baconstyle"/>
def create_baconstyle_el():
   namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
   tag = namespace + 'rStyle'
   ns_val = namespace + 'val'
   el = xml.etree.ElementTree.Element(tag)
   el.attrib[ns_val] = "baconstyle"
   return el

#nahraje styl do elementu, který má bit = 1
def bacon_element(prop_el,bit,namespace):
   if bit == "1":
# apply <w:rStyle w:val="baconstyle"/>  
      for subelement in prop_el[:]:
         # print(subelement.tag)
         #namespaces které musím odstranit, kvůli kolizím s mým vlastním stylem
         if(subelement.tag == namespace + "rFonts"):
            prop_el.remove(subelement)
         elif(subelement.tag == namespace + "szC"):
            prop_el.remove(subelement)
         elif(subelement.tag == namespace + "sz"):
            prop_el.remove(subelement)
      #nahrání změn na místa kde je ukrytá zpráva (tzn. bit 1)         
      style_el = create_baconstyle_el()
      prop_el.append(style_el)

#do dokumentu docx se nahraje můj vlastní styl, který později použiji pro ukrytí zprávy
def add_bacon_style(font_styles):
   #check jestli styl již existuje, nelze přidat 2x
   custom_style_present = False
   for style in font_styles:
      if 'bold_style' == style.name:
         custom_style_present = True
   #nastavení custom stylu
   if not custom_style_present:
      font_charstyle = font_styles.add_style('baconstyle', WD_STYLE_TYPE.CHARACTER)
      font_object = font_charstyle.font
      font_object.size = Pt(10)
      font_object.name = 'Century Schoolbook'