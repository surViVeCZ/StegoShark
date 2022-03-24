from email import message
from email.errors import CharsetError
from operator import index
import sys, getopt
from xml.dom.minidom import Element
import docx
from docx.shared import Length
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

def count_spaces(text):
    cnt = 0
    for i in range(0, len(text)):
        if text[i] == " ":
            cnt += 1
    return cnt

def Spaces_encode(file, message):
    binary_mes = steganography.str_to_binary(message)
    print(binary_mes)
    print("\n", end='')

    #nutno zjistit počet slov, více slov umožňuje ukrytí delší zprávy
    full_text = steganography.print_text(file)

    word_list = full_text.split()
    number_of_spaces = count_spaces(full_text)

    #pro ukrytí jednoho znaku je potřeba 8 znaků cover textu
    if(len(message*8) > number_of_spaces):
        print("Cover text doesn't have enough capacity to hide this message")
        return False

    path = xml_parse.split_document(binary_mes, file, "spaces")
    return path
    
def Spaces_decode(file):
    try:
        doc = Document(file)
    except:
        print("Non existing file")
        sys.exit()

    font_styles = doc.styles
    binary = "" #bold = 1, nonbold = 0
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run.style.name == "spaces_style":
                binary = binary + '1';
            elif run.text == " ":
                binary = binary + '0';
           
    secret_message = steganography.binary_to_str(binary)
    return secret_message

def create_whitespace_el():
   namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
   tag = namespace + 'sz'
   ns_val = namespace + 'val'
   el = xml.etree.ElementTree.Element(tag)
   el.attrib[ns_val] = "19" #hodnota mezery odpovídá fontu velikosti 9,5
   return el

def create_tag():
    namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    tag = namespace + 'rStyle'
    ns_val = namespace + 'val'
    el = xml.etree.ElementTree.Element(tag)
    el.attrib[ns_val] = "spaces_style"
    return el

#nahraje styl do elementu, který má bit = 1
def spaces_element(prop_el,bit,namespace):
    if bit == "1":
        for subelement in prop_el[:]:
            if(subelement.tag == namespace + "sz"):
                prop_el.remove(subelement)
        style_el = create_whitespace_el()
        style_tag = create_tag()
        prop_el.append(style_tag)
        prop_el.append(style_el)

#do dokumentu docx se nahraje můj vlastní styl, který později použiji pro ukrytí zprávy
#tento styl neobsahuje žádné vlastnosti, souží pouze jako flag, abych poznal kde je urkytá zpráva
def add_spaces_style(font_styles):
   #check jestli styl již existuje, nelze přidat 2x
   custom_style_present = False
   for style in font_styles:
      if 'spaces_style' == style.name:
         custom_style_present = True
   #nastavení custom stylu
   if not custom_style_present:
      font_charstyle = font_styles.add_style('spaces_style', WD_STYLE_TYPE.CHARACTER)