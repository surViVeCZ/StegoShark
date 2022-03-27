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

#moduly
import bacon
import whitespaces
import xml_parse
import synonyms

class SplitDocument:
   doc_ref = ""
   paragraphs = []
   secret_message = ""

def updateZip(zipname, zip_file_location, outside_file_location):
   # generate a temp file
   tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
   os.close(tmpfd)

   #vytvoří kopii archivu           
   with zipfile.ZipFile(zipname, 'r') as zin:
      with zipfile.ZipFile(tmpname, 'w') as zout:
         zout.comment = zin.comment 
         for item in zin.infolist():
               if item.filename != zip_file_location:
                  zout.writestr(item, zin.read(item.filename))

   #nahrazení
   os.remove(zipname)
   os.rename(tmpname, zipname)

   #přidání filename včetně dat
   with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
      zf.write(outside_file_location, zip_file_location)

# todo zkontrolovat mezery
def split_to_words(string):
   word = string.strip().split()
   return(word)


#cite: https://stackoverflow.com/questions/8733233/filtering-out-certain-bytes-in-python
#author: https://stackoverflow.com/users/84270/john-machin
def valid_xml_char_ordinal(c):
    codepoint = ord(c)
    # conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
        )

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
   replace = False
   own1 = False

# zpracování vstupních argumentů
def ArgumentsParsing(argv):
   #načtení defaultních hodnot
   cfg = Config()
   try:
      opts, args = getopt.getopt(argv,"i:ed:s:bwro",['ifile=','encode','decode','message','bacon','whitespaces','replace','own1'])
   except getopt.GetoptError:
     print("steganography.py -i <inputfile> -e/-d -s <secret_message> -<b/w/r>/--own1")
     sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
        rint("steganography.py -i <inputfile> -e/-d -s <secret_message> -<b/w/r>/--own1")
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
      elif opt in ('-r','--replace'):
         cfg.replace = True
      elif opt in ('-o','--own1'):
         cfg.own1 = True
   return cfg

def main(argv):

   cfg = ArgumentsParsing(argv)

   if(cfg.bacon is False and cfg.whitespaces is False and cfg.replace is False and cfg.own1 is False):
      print("Wrong parameters, use -h for help")
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
            secret_message = bacon.Bacon_decode(cfg.inputfile)
         elif(cfg.whitespaces is True):
            secret_message = whitespaces.Spaces_decode(cfg.inputfile)
         elif(cfg.replace is True):
            secret_message = synonyms.syn_decode(cfg.inputfile, "default")
         elif(cfg.own1 is True):
            secret_message = synonyms.syn_decode(cfg.inputfile, "own1") 
         print("The secret message is:", secret_message)
         print("\n", end='')

         file_path = cfg.inputfile.replace("encoded", "decoded")
         #vytvoření a zápis do souboru 
         try:
            decoded_file = docx.Document()
         except:
            print("Non existing file")
            sys.exit()

         if(secret_message  is not None):
            cleaned_string = ''.join(c for c in secret_message if valid_xml_char_ordinal(c))
            decoded_file.add_paragraph(cleaned_string)
         decoded_file.save(file_path)
         
      elif(cfg.encode == True):
         if(cfg.message == ''):
            print("To encode you need to use parameter -s for secret message")
            sys.exit()
   
         if(cfg.bacon is True):
            file_path = bacon.Bacon_encode(cfg.inputfile, cfg.message)
            if file_path is False:
               return False
         elif(cfg.whitespaces is True):
            file_path = whitespaces.Spaces_encode(cfg.inputfile, cfg.message)
            if file_path is False:
               return False
         elif(cfg.replace is True):
            #default = klasické kódování 8bit
            file_path = synonyms.syn_encode(cfg.inputfile, cfg.message, "default")
            if file_path is False:
               return False
         elif(cfg.own1 is True):
            #own1 = metoda synonym za využití Baconova kódování, tzn. 5bit
            file_path = synonyms.syn_encode(cfg.inputfile, cfg.message, "own1")
            if file_path is False:
               return False

      # print(print_text(cfg.inputfile))
      

   #vstupní cover text je txt, txt soubor je nahrát a zpracován jako dokument docx
   elif(cfg.inputfile.endswith('.txt')):
      text = Reading_txt(cfg.inputfile)
      print(text)

      #převedení
      txt_to_docx = docx.Document()
      txt_to_docx.add_paragraph(text)
      
      name_docx = cfg.inputfile.split('.txt')
      txt_to_docx.save(name_docx[0]+'.docx')

      bacon.Bacon_encode(name_docx[0]+'.docx', cfg.message)
   else:
      print("Wrong input file")
      sys.exit()
      
   # uložení tajné zprávy do souboru: {path}, zakódované zprávy jsou uložené ve složce encoded, dekódované ve složce decoded
   print ("Output file: {0}" .format(file_path))

if __name__ == "__main__":
   main(sys.argv[1:])
     

