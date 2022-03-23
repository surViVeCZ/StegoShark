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
import collections


dictionary_of_zeros =    collections.OrderedDict((("want",{0}),("easy",{0}),("still",{0}),("hardworking",{0}),("buy",{0}),("smart",{0}),("strong",{0}),("stupid",{0}),("essential",{0}),("irrelevant",{0}),
                        ("excellent",{0}),("acceptable",{0}),("awful",{0}),("interesting",{0}),("boring",{0}),("uncertain",{0}),("difficult",{0}),("weak",{0}),("many",{0}),("bit",{0}),
                        ("huge",{0}),("tiny",{0}),("new",{0}),("old",{0}),("excess",{0}),("alert",{0}),("short",{0}),("abuse",{0}),("unreliable",{0}),("puzzle",{0}),("lethargy",{0}),
                        ("representative",{0}),("lie",{0}),("fanatic",{0}),("enthusiasm",{0}),("require",{0}),("rest",{0}),("refuse",{0}),("thoughtful",{0}),("undecided",{0}),
                        ("motive",{0}),("reject",{0}),("expect",{0}),("terrible",{0}),("plentiful",{0}),("introduce",{0}),("change",{0}),("real",{0}),("negative",{0}),("positive",{0}),
                        ("progress",{0}),("admit",{0}),("about",{0}),("wide",{0}),("break",{0}),("correct",{0}),("decide",{0}),("certain",{0}),("do",{0}),("leave",{0}),("different",{0}),
                        ("reveal",{0}),("explain",{0}),("extra",{0}),("false",{0}),("famous",{0}),("great",{0}),("collect",{0}),("get",{0}),("help",{0}),("have",{0}),("hide",{0}),("idea",{0}),
                        ("ignore",{0}),("last",{0}),("mainly",{0}),("label",{0}),("material",{0}),("mix",{0}),("inform",{0}),("strange",{0}),("abroad",{0}),("place",{0}),("provide",{0}),
                        ("quick",{0}),("quiet",{0}),("rare",{0}),("safe",{0}),("stable",{0}),("divide",{0}),("think",{0}),("try",{0}),("illegal",{0}),("usually",{0}),("huge",{0}),
                        ("imagine",{0}),("value",{0}),("amazing",{0}),("empty",{0}),("decrease",{0}),("use",{0}),("good",{0}),("high",{0}),("fast",{0}),("thick",{0}),("accept",{0}),("funny",{0}),
                        ("plan",{0}),("catch",{0}),("contain",{0}),("gather",{0}),("live",{0}),("connect",{0}),("cold",{0}),("cut",{0}),("fall",{0}),("trip",{0}),("near",{0}),("under",{0}),
                        ("same",{0}),("benefit",{0}),("abandon",{0}),("obvious",{0}),("result",{0}),("offer",{0}),("extreme",{0}),("festival",{0}),("humble",{0}),("opponent",{0}),("secret",{0}),
                        ("negotiate",{0}),("violate",{0}),("stubborn",{0}),("adjust",{0}),("dry",{0}),("experimental",{0}),("important",{0}),("see",{0}),("also",{0}),("rude",{0}),("hot",{0}),
                        ("poor",{0}),("shy",{0}),("decline",{0}),("fake",{0}),("tasty",{0}),("prolong",{0}),("clever",{0})))

dictionary_of_synonyms = collections.OrderedDict((("wish",{1}),("uncomplicated",{1}),("perennially",{1}),("assiduous",{1}),("purchase",{1}),("wise",{1}),("firm",{1}),("dimwitted",{1}),("indispensable",{1}),("insignificant",{1}),
                        ("magnificent",{1}),("adequate",{1}),("atrocious",{1}),("intriguing",{1}),("tiresome",{1}),("dubious",{1}),("daunting",{1}),("feeble",{1}),("ample",{1}),("smitgen",{1}),
                        ("immense",{1}),("dinky",{1}),("contemporary",{1}),("obsolete",{1}),("surplus",{1}),("watchful",{1}),("brief",{1}),("vituperate",{1}),("incredulous",{1}),("enigma",{1}),
                        ("laxity",{1}),("delegate",{1}),("prevaricate",{1}),("zeelot",{1}),("zest",{1}),("yearn",{1}),("repose",{1}),("deny",{1}),("considerate",{1}),("irresolute",{1}),
                        ("intention",{1}),("quash",{1}),("anticipate",{1}),("tremendous",{1}),("abundant",{1}),("acquaint",{1}),("alter",{1}),("genuine",{1}),("adverse",{1}),("affirmative",{1}),
                        ("advance",{1}),("confess",{1}),("approximately",{1}),("broad",{1}),("fracture",{1}),("right",{1}),("determine",{1}),("definite",{1}),("execute",{1}),("depart",{1}),
                        ("diverse",{1}),("disclose",{1}),("clarify",{1}),("additional",{1}),("untrue",{1}),("renowned",{1}),("stunning",{1}),("gather",{1}),("obtain",{1}),("support",{1}),("own",{1}),
                        ("conceal",{1}),("thought",{1}),("disregard",{1}),("final",{1}),("chiefly",{1}),("mark",{1}),("fabric",{1}),("blend",{1}),("notify",{1}),("odd",{1}),("overseas",{1}),("spot",{1}),
                        ("supply",{1}),("rapid",{1}),("peaceful",{1}),("scarce",{1}),("secure",{1}),("steady",{1}),("split",{1}),("consider",{1}),("attempt",{1}),("unlawful",{1}),("generally",{1}),
                        ("visualise",{1}),("worth",{1}),("miraculous",{1}),("blank",{1}),("shrink",{1}),("employ",{1}),("satisfying",{1}),("elevated",{1}),("swift",{1}),("dense",{1}),
                        ("approve",{1}),("amusing",{1}),("procedure",{1}),("capture",{1}),("comprise",{1}),("accumulate",{1}),("dwell",{1}),("join",{1}),("chilly",{1}),("chop",{1}),("drop",{1}),("journey",{1}),
                        ("close",{1}),("below",{1}),("alike",{1}),("profit",{1}),("forsake",{1}),("evident",{1}),("outcome",{1}),("proffer",{1}),("excessive",{1}),("feast",{1}),("modest",{1}),("rival",{1}),
                        ("furtive",{1}),("settle",{1}),("infringe",{1}),("contumacy",{1}),("reconcile",{1}),("arid",{1}),("tentative",{1}),("vital",{1}),("observe",{1}),("furthermore",{1}),("vulgar",{1}),
                        ("scalding",{1}),("destitute",{1}),("bashful",{1}),("wane",{1}),("sham",{1}),("scrumptious",{1}),("prolix",{1}),("canny",{1})))

def count_dictionary_words(text):
    cnt = 0
    words = text.split()
    for word in words:
        if word in dictionary_of_zeros:
            cnt += 1
    return cnt


def syn_encode(file, message):

    print(len(dictionary_of_synonyms))
    print(len(dictionary_of_zeros))
    binary_mes = steganography.str_to_binary(message)
    print(binary_mes)
    print("\n", end='')
  
    full_text = steganography.print_text(file)
    word_list = full_text.split()
    number_of_words = len(re.findall(r'\w+', full_text))


    #pro ukrytí jednoho znaku je potřeba 8 znaků cover textu
    words_available = count_dictionary_words(full_text)
  
    if(len(message*8) > words_available):
        print("Cover text doesn't have enough capacity to hide this message")
        sys.exit()


    combined = list(zip(dictionary_of_zeros, dictionary_of_synonyms))
    for couple in combined:
        print(couple)

    path = xml_parse.split_document(binary_mes, file, "synonyms")
    return path


def syn_decode(file):
    try:
      doc = Document(file)
    except:
      print("Non existing file")
      sys.exit()

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
                word = word.lower()
                if ((word in dictionary_of_synonyms) and (run.style.name != "skip")):
                    binary += "1"
                elif word in dictionary_of_zeros:
                    binary += "0"

    # print(binary)
    secret_message = steganography.binary_to_str(binary)
    return secret_message

 
# returns <w:rStyle w:val="synonym_element"/>
def create_syn_tag():
   namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
   tag = namespace + 'rStyle'
   ns_val = namespace + 'val'
   el = xml.etree.ElementTree.Element(tag)
   el.attrib[ns_val] = "synonym_element"
   return el

# returns <w:rStyle w:val="skip"/>
#pokud je nějaké slovo z původního cover textu již obsaženo v mém slovníku dictionary_of_synonym, je zapotřebí tohle slovo vynechat,
#aby nevznikaly jedničkové bity na nechtěných místech
def skip_tag():
   namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
   tag = namespace + 'rStyle'
   ns_val = namespace + 'val'
   el = xml.etree.ElementTree.Element(tag)
   el.attrib[ns_val] = "skip"
   return el

def add_skip_tag(font_styles):
   custom_style_present = False
   for style in font_styles:
      if 'skip' == style.name:
        custom_style_present = True
   #nastavení custom stylu
   if not custom_style_present:
      font_charstyle = font_styles.add_style('skip', WD_STYLE_TYPE.CHARACTER)

#nahraje styl do elementu, který se má přeskočit
def syn_element(prop_el,bit,namespace, word, run):
    syn_word = word

    #na všechny slova, která se vyzkytují ve slovníku přiřadím tag, pouze těmto slovům budu přidělovat bity
    if(word.lower() in dictionary_of_zeros):
        index = list(dictionary_of_zeros.keys()).index(word.lower())

        #jedničkové bity nahradím jejich synonymem
        if bit == '1':
            print("\n", end='')
            print("replacing....")  

            #nalezení příslušného synonyma ve druhém slovníku, podle indexu
            syn_word = list(dictionary_of_synonyms.keys())[index]
            
            print("index in dict: %d (%s)" % (index, word))
            print("syn in dict: %d (%s)" % (index, syn_word))
            print("\n", end='')

        
        #pokud bylo původní slovo napsané velkými písmeny, nové musí být také
        if (word.isupper()):
            syn_word = syn_word.upper()

        # apply <w:rStyle w:val="synonym"/>  
        for subelement in prop_el[:]: 
            tag = create_syn_tag()
        prop_el.append(tag)
       
       

    elif(word.lower() in dictionary_of_synonyms):
        # apply <w:rStyle w:val="skip"/>  
        for subelement in prop_el[:]: 
            tag = skip_tag()
        prop_el.append(tag)

    return syn_word



