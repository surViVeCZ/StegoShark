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

def Spaces_encode(file, message):
    binary_mes = steganography.str_to_binary(message)
    print(binary_mes)

    #nutno zjistit počet slov, více slov umožňuje ukrytí delší zprávy
    full_text = steganography.print_text(file)

    word_list = full_text.split()
    number_of_words = len(re.findall(r'\w+', full_text))

    #pro ukrytí jednoho znaku je potřeba 8 znaků cover textu
    if(len(message*8) > number_of_words):
        print("Cover text doesn't have enough capacity to hide this message")
        sys.exit()

    path = xml_parse.split_document(binary_mes, file, "spaces")
    return path
    

# returns <w:sz w:val="baconstyle"/>
def create_whitespace_el():
   namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
   tag = namespace + 'sz'
   ns_val = namespace + 'val'
   el = xml.etree.ElementTree.Element(tag)
   el.attrib[ns_val] = "19" #hodnota mezery odpovídá fontu velikosti 9,5
   return el

#nahraje styl do elementu, který má bit = 1
def spaces_element(prop_el,bit,namespace):
    if bit == "1":
        for subelement in prop_el[:]:
            if(subelement.tag == namespace + "sz"):
                prop_el.remove(subelement)
        style_el = create_whitespace_el()
        prop_el.append(style_el)