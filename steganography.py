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
import docx
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.style import WD_STYLE_TYPE
from termcolor import colored
import numpy as np
import re
import os
import string

bacons_table = ["00000", "00001", "00010", "00011", "00100", "00101", "00110", "00111", "01000",
               "01001", "01010", "01011", "01100", "01101", "01110", "01111", "10000", "10001", "10010",
               "10011", "10100", "10101", "10110", "10111"]

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "(I,J)", "K", "L", "M", "N", "O", "P","Q",
            "R", "S", "T", "(U/V)", "W", "X", "Y", "Z"]


class SplitDocument:
   doc_ref = ""
   paragraphs = []
   secret_message = ""

class Par:
   runs = []

#původní dokument se rozloží na odstavce,runy a slova, ty se následně z jiným stylem uloží do nového dokumentu
def split_document(doc,message_pattern,file):
   new_doc = docx.Document()
   message_len = len(message_pattern)
   message_end = False

   msg_iter = iter(message_pattern)

   for paragraph in doc.paragraphs:
      par = new_doc.add_paragraph()
      for run in paragraph.runs:
         words = run.text.strip().split(" ")

         #kvůli zipu se nedopíše zbytek
         for word in words:
            bit = next(msg_iter, None)

            if bit is None:
               par.add_run(word +" ")
               message_end = True
            elif(bit == '0'):
               par.add_run(word +" ")
            elif(bit == '1'):
               par.add_run(word +" ").bold = True
  
   save_path = 'encoded'
   file_name = 'encoded_'+file


   try:
      full_path = os.path.join(save_path, file_name)
   except:
      print("Non existing path")
      sys.exit()
   print(full_path)

   
   new_doc.save(full_path)



def listToString(s): 
    string = ""
    for ch in s: 
        string += ch  
    return string 

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


def print_text(file):
   complete_text = []
   doc = docx.Document(file)
   for paragraph in doc.paragraphs:
      complete_text.append(paragraph.text)
   cover_text = '\n'.join(complete_text)
   return cover_text

#ukrytí tajné zprávy pomocí Baconovy šifry
def Bacon_encode(file, message):
   
   doc = docx.Document(file)
   binary_message = str_to_binary(message)
   print("Binary message: " + binary_message)

   message = split(message)
   message_string = listToString(message)
   print(message)

   index_array = []
   for i in range(len(message)):
      index_array.append(string.ascii_lowercase.index(message[i]))
   print(index_array)
  

   message_pattern = []
   for k in index_array:
      #nutné upravit hodnoty indexů, kvůli dvojicím i,j a u,v (mají stejný vzor v Baconově šifře)
      if(k > 8 and k < 19):
         k -= 1
      elif(k > 19):
         k -= 2
      message_pattern.append(bacons_table[k])

   
   pattern_string = listToString(message_pattern)
   print(message_pattern,pattern_string)
   print("\n", end='')

   #nutno zjistit počet slov, více slov umožňuje ukrytí delší zprávy
   full_text = print_text(file)
   word_list = full_text.split()
   number_of_words = len(word_list)
   
   # print(len(binary_message))
   # print(number_of_words)
   if(len(binary_message) > number_of_words):
      print("Cover text doesn't have enough capacity to hide this message")
      sys.exit()
   
   split_document(doc,pattern_string, file)

   # parag = doc.add_paragraph("Hello!")
   # font_styles = doc.styles

   # #stzl se již nachází v souboru
   # custom_style_present = False
   # for style in font_styles:
   #    if 'bold_style' == style.name:
   #       custom_style_present = True

   # #nastavení custom sytlu
   # if not custom_style_present:
   #    font_charstyle = font_styles.add_style('bold_style', WD_STYLE_TYPE.CHARACTER)
   #    font_object = font_charstyle.font
   #    font_object.size = Pt(15)
   #    font_object.name = 'Times New Roman'

   # parag.add_run("BOLD", style='bold_style').bold=True
   # parag.add_run("Nonbold")


      
def Bacon_decode(file):
   try:
      doc = docx.Document(file)
   except:
      print("Non existing file")
      sys.exit()

   bold_words = []
   non_bold = []
   binary = "" #bold = 1, nonbold = 0
   text = ""

   #rozdělí text na tučné a obyčejné slova
   for paragraph in doc.paragraphs:
      text = text + paragraph.text + " "

      for run in paragraph.runs:
         # #pro kódování a dekódování Baconovou šifrou nepracuji s bílými znaky (pro práci s nimi je implementována jiná metoda)
         for word in run.text.strip().split(" "):
            if run.bold:
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

# zpracování vstupních argumentů
def ArgumentsParsing(argv):
       
   #načtení defaultních hodnot
   cfg = Config()
   try:
      opts, args = getopt.getopt(sys.argv[1:],"i:ed:m:",['ifile=','encode','decode','message'])
   except getopt.GetoptError:
     print("steganography.py -i <inputfile> -o <outputfile> -e/-d -m <message>")
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
      elif opt in ('-m', '--message'):
         cfg.message = arg
   return cfg

def main(argv):

   cfg = ArgumentsParsing(argv)

   print("\n", end='')
   print ("Input file: {0}" .format(cfg.inputfile))

   #vstupní cover text je docs
   if(cfg.inputfile.endswith('.docx')):
      print("\n", end='')

      #Dekódování Baconovou šifrou
      if(cfg.decode == True):
         secret_message = Bacon_decode(cfg.inputfile)
         print("The secret message is:", secret_message)
         print("\n", end='')

         #dekódované zprávy jsou uložené ve složce decoded
         save_path = 'decoded'
         file_name = 'decoded_'+cfg.inputfile

        
        
         file_path = cfg.inputfile.replace("encoded", "decoded")
      

     
         # full_path = os.path.join(save_path, file_name)

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
            print("To encode you need to use parameter -m for secret message")
            sys.exit()
         Bacon_encode(cfg.inputfile, cfg.message)

         #zakódované zprávy jsou uložené ve složce encoded
         save_path = 'encoded'
         file_name = 'encoded_'+cfg.inputfile

     
         file_path = os.path.join(save_path, file_name)

      print(print_text(cfg.inputfile))
      

   #vstupní cover text je txt, txt soubor je nahrát a zpracován jako dokument docx
   elif(cfg.inputfile.endswith('.txt')):
      text = Reading_txt(cfg.inputfile)
      print(text)

      #převedení
      txt_to_docx = docx.Document()
      txt_to_docx.add_paragraph(text)
      
      name_docx = cfg.inputfile.split('.txt')
      txt_to_docx.save(name_docx[0]+'_new.docx')

   # uložení tajné zprávy do souboru: {path}
   print("\n", end='')
   print ("Output file: {0}" .format(file_path))

if __name__ == "__main__":
   main(sys.argv[1:])
     

