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
         zout.comment = zin.comment # preserve the comment
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
   # return [word for word in string.strip().split() if not word == '' and not word == ' ' ]


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

# zpracování vstupních argumentů
def ArgumentsParsing(argv):
   #načtení defaultních hodnot
   cfg = Config()
   try:
      opts, args = getopt.getopt(sys.argv[1:],"i:ed:s:bwr",['ifile=','encode','decode','message','bacon','whitespaces','replace'])
   except getopt.GetoptError:
     print("steganography.py -i <inputfile> -e/-d -s <secret_message> -<b/w/r>")
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
      elif opt in ('-r','--replace'):
         cfg.replace = True
   return cfg

def main(argv):

   cfg = ArgumentsParsing(argv)

   if(cfg.bacon is False and cfg.whitespaces is False and cfg.replace is False):
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
            secret_message = synonyms.syn_decode(cfg.inputfile)
         print("The secret message is:", secret_message)
         print("\n", end='')

         file_path = cfg.inputfile.replace("encoded", "decoded")

         #vytvoření a zápis do souboru 
         try:
            decoded_file = open(file_path, "w")
         except:
            print("Non existing file")
            sys.exit()

         if(secret_message  is not None):
            decoded_file.write(secret_message)
         decoded_file.close()
         
      elif(cfg.encode == True):
         if(cfg.message == ''):
            print("To encode you need to use parameter -s for secret message")
            sys.exit()
   
         if(cfg.bacon is True):
            file_path = bacon.Bacon_encode(cfg.inputfile, cfg.message)
         elif(cfg.whitespaces is True):
            file_path = whitespaces.Spaces_encode(cfg.inputfile, cfg.message)
         elif(cfg.replace is True):
            file_path = synonyms.syn_encode(cfg.inputfile, cfg.message)


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
     
