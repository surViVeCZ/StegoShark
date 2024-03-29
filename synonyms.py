# ----------------------------------------------------------------------
# Autor:          Petr Pouč
# Login:          xpoucp01
# Datum:          27.04.2022
# Název práce:    Digitální textová steganografie
# Cíl práce:      Implementace 4 vybraných steganografických metod
# ----------------------------------------------------------------------


from docx import Document
from termcolor import colored
import re
import string
import xml.etree.ElementTree
import xml.dom.minidom
import steganography
import xml_parse
import collections

import steganography
import bacon
import error_handler
import huffman_coding

# @brief slovník slov, které představují "0" bit
dictionary_of_zeros = collections.OrderedDict((("want", {0}), ("easy", {0}), ("still", {0}), ("hardworking", {0}), ("buy", {0}), ("smart", {0}), ("strong", {0}), ("stupid", {0}), ("essential", {0}), ("irrelevant", {0}),
                                               ("excellent", {0}), ("acceptable", {0}), ("awful", {0}), ("interesting", {0}), ("boring", {
                                                   0}), ("uncertain", {0}), ("difficult", {0}), ("weak", {0}), ("many", {0}), ("bit", {0}),
                                               ("huge", {0}), ("tiny", {0}), ("new", {0}), ("old", {0}), ("excess", {0}), ("alert", {
                                                   0}), ("short", {0}), ("abuse", {0}), ("unreliable", {0}), ("puzzle", {0}), ("lethargy", {0}),
                                               ("representative", {0}), ("lie", {0}), ("fanatic", {0}), ("enthusiasm", {0}), ("require", {
                                                   0}), ("rest", {0}), ("refuse", {0}), ("thoughtful", {0}), ("undecided", {0}),
                                               ("motive", {0}), ("reject", {0}), ("expect", {0}), ("terrible", {0}), ("plentiful", {
                                                   0}), ("introduce", {0}), ("change", {0}), ("real", {0}), ("negative", {0}), ("positive", {0}),
                                               ("progress", {0}), ("admit", {0}), ("about", {0}), ("wide", {0}), ("break", {0}), ("correct", {
                                                   0}), ("decide", {0}), ("certain", {0}), ("do", {0}), ("leave", {0}), ("different", {0}),
                                               ("reveal", {0}), ("explain", {0}), ("extra", {0}), ("false", {0}), ("famous", {0}), ("great", {
                                                   0}), ("collect", {0}), ("get", {0}), ("help", {0}), ("have", {0}), ("hide", {0}), ("idea", {0}),
                                               ("ignore", {0}), ("last", {0}), ("mainly", {0}), ("label", {0}), ("material", {0}), ("mix", {
                                                   0}), ("inform", {0}), ("strange", {0}), ("abroad", {0}), ("place", {0}), ("provide", {0}),
                                               ("quick", {0}), ("quiet", {0}), ("rare", {0}), ("safe", {0}), ("stable", {0}), ("divide", {
                                                   0}), ("think", {0}), ("try", {0}), ("illegal", {0}), ("usually", {0}), ("huge", {0}),
                                               ("imagine", {0}), ("value", {0}), ("amazing", {0}), ("empty", {0}), ("decrease", {0}), ("use", {
                                                   0}), ("good", {0}), ("high", {0}), ("fast", {0}), ("thick", {0}), ("accept", {0}), ("funny", {0}),
                                               ("plan", {0}), ("catch", {0}), ("contain", {0}), ("gather", {0}), ("live", {0}), ("connect", {
                                                   0}), ("cold", {0}), ("cut", {0}), ("fall", {0}), ("trip", {0}), ("near", {0}), ("under", {0}),
                                               ("same", {0}), ("benefit", {0}), ("abandon", {0}), ("obvious", {0}), ("result", {0}), ("offer", {
                                                   0}), ("extreme", {0}), ("festival", {0}), ("humble", {0}), ("opponent", {0}), ("secret", {0}),
                                               ("negotiate", {0}), ("violate", {0}), ("stubborn", {0}), ("adjust", {0}), ("dry", {
                                                   0}), ("experimental", {0}), ("important", {0}), ("see", {0}), ("also", {0}), ("rude", {0}), ("hot", {0}),
                                               ("poor", {0}), ("shy", {0}), ("decline", {0}), ("fake", {0}), ("tasty", {0}), ("prolong", {0}), ("clever", {0})))

# @brief slovník synonym představující "1" bit
dictionary_of_synonyms = collections.OrderedDict((("wish", {1}), ("uncomplicated", {1}), ("perennially", {1}), ("assiduous", {1}), ("purchase", {1}), ("wise", {1}), ("firm", {1}), ("dimwitted", {1}), ("indispensable", {1}), ("insignificant", {1}),
                                                  ("magnificent", {1}), ("adequate", {1}), ("atrocious", {1}), ("intriguing", {1}), ("tiresome", {
                                                      1}), ("dubious", {1}), ("daunting", {1}), ("feeble", {1}), ("ample", {1}), ("smitgen", {1}),
                                                  ("immense", {1}), ("dinky", {1}), ("contemporary", {1}), ("obsolete", {1}), ("surplus", {
                                                      1}), ("watchful", {1}), ("brief", {1}), ("vituperate", {1}), ("incredulous", {1}), ("enigma", {1}),
                                                  ("laxity", {1}), ("delegate", {1}), ("prevaricate", {1}), ("zeelot", {1}), ("zest", {
                                                      1}), ("yearn", {1}), ("repose", {1}), ("deny", {1}), ("considerate", {1}), ("irresolute", {1}),
                                                  ("intention", {1}), ("quash", {1}), ("anticipate", {1}), ("tremendous", {1}), ("abundant", {
                                                      1}), ("acquaint", {1}), ("alter", {1}), ("genuine", {1}), ("adverse", {1}), ("affirmative", {1}),
                                                  ("advance", {1}), ("confess", {1}), ("approximately", {1}), ("broad", {1}), ("fracture", {
                                                      1}), ("right", {1}), ("determine", {1}), ("definite", {1}), ("execute", {1}), ("depart", {1}),
                                                  ("diverse", {1}), ("disclose", {1}), ("clarify", {1}), ("additional", {1}), ("untrue", {1}), ("renowned", {
                                                      1}), ("stunning", {1}), ("gather", {1}), ("obtain", {1}), ("support", {1}), ("own", {1}),
                                                  ("conceal", {1}), ("thought", {1}), ("disregard", {1}), ("final", {1}), ("chiefly", {1}), ("mark", {
                                                      1}), ("fabric", {1}), ("blend", {1}), ("notify", {1}), ("odd", {1}), ("overseas", {1}), ("spot", {1}),
                                                  ("supply", {1}), ("rapid", {1}), ("peaceful", {1}), ("scarce", {1}), ("secure", {1}), ("steady", {
                                                      1}), ("split", {1}), ("consider", {1}), ("attempt", {1}), ("unlawful", {1}), ("generally", {1}),
                                                  ("visualise", {1}), ("worth", {1}), ("miraculous", {1}), ("blank", {1}), ("shrink", {
                                                      1}), ("employ", {1}), ("satisfying", {1}), ("elevated", {1}), ("swift", {1}), ("dense", {1}),
                                                  ("approve", {1}), ("amusing", {1}), ("procedure", {1}), ("capture", {1}), ("comprise", {1}), ("accumulate", {
                                                      1}), ("dwell", {1}), ("join", {1}), ("chilly", {1}), ("chop", {1}), ("drop", {1}), ("journey", {1}),
                                                  ("close", {1}), ("below", {1}), ("alike", {1}), ("profit", {1}), ("forsake", {1}), ("evident", {
                                                      1}), ("outcome", {1}), ("proffer", {1}), ("excessive", {1}), ("feast", {1}), ("modest", {1}), ("rival", {1}),
                                                  ("furtive", {1}), ("settle", {1}), ("infringe", {1}), ("contumacy", {1}), ("reconcile", {1}), ("arid", {
                                                      1}), ("tentative", {1}), ("vital", {1}), ("observe", {1}), ("furthermore", {1}), ("vulgar", {1}),
                                                  ("scalding", {1}), ("destitute", {1}), ("bashful", {1}), ("wane", {1}), ("sham", {1}), ("scrumptious", {1}), ("prolix", {1}), ("canny", {1})))

# @brief spočítá kolik slov v textu je součástí mých slovníků
# @param text text souboru
# @return počet slovníkových slov
# @note funkci používám, abych zjistil, zda-li má text dostatek slov na ukrytí zvolené tajné zprávy


def count_dictionary_words(text: str) -> int:
    cnt = 0
    words = text.split()
    for word in words:
        if word in dictionary_of_zeros:
            cnt += 1
    return cnt


class syn_cipher:
    def __init__(self, file: str, message: str):
        self.file = file
        self.message = message
    # @brief ukrytí tajné zprávy pomocí metody synonym
    # @param file vstupní cover soubor
    # @param message tajná zpráva, kterou si přejeme ukrýt
    # @param bits určuje druh šifrování (8-bit ASCII, Bacon, Huffman)
    # @return cesta k zašifrovanému souboru

    def syn_encode(self, file: str, message: str, bits: int) -> str:
        if (bits == "default"):
            binary_mes = steganography.str_to_binary(message)

        if (bits == "own2"):
            binary_mes = huffman_coding.get_frequency(message)
            print(binary_mes)
            print(len(binary_mes))

        full_text = steganography.print_text(file)
        # pro ukrytí jednoho znaku je potřeba 8 znaků cover textu
        words_available = count_dictionary_words(full_text)
        if (bits == "default"):
            if (len(message)*8 > words_available):
                print("Cover text doesn't have enough capacity to hide this message")
                return False
        # pro ukrytí je zapotřebí pouhých 5 bitů
        elif (bits == "own1"):
            if (len(message)*5 > words_available):
                print("Cover text doesn't have enough capacity to hide this message")
                return False
        elif (bits == "own2"):
            if (len(binary_mes) > words_available):
                print("Cover text doesn't have enough capacity to hide this message")
                return False

        # vlastní varianta metody (s využitím Baconova šifrování)
        if (bits == "own1"):
            message = steganography.split(message)

            index_array = []
            for ch in message:
                try:
                    index_array.append(string.ascii_lowercase.index(ch))
                except:
                    index_array.append(bacon.alphabet.index(ch))
            print(index_array)

            message_pattern = []
            for k in index_array:
                if (k == 24):
                    pass
                else:
                    # nutné upravit hodnoty indexů, kvůli dvojicím i,j a u,v (mají stejný vzor v Baconově šifře)
                    if (k > 8 and k <= 19):
                        k -= 1
                    elif (k == 20):
                        k -= 1
                    elif (k > 20 < 24):
                        k -= 2
                message_pattern.append(bacon.bacons_table[k])
            binary_mes = steganography.listToString(message_pattern)

        split_obj = xml_parse.XML_split(binary_mes, file, "synonyms", bits)
        path = split_obj.split_document()

        return path

    # @brief dešifrování pomocí metody synonym
    # @param file zašifrovaný soubor
    # @param bits určuje druh šifrování (8-bit ASCII, Bacon, Huffman)
    # @return tajná zpráva
    # @note správně dešifrovat můžeme pouze soubory zašifrované stejnou metodou

    def syn_decode(self, file: str, bits: int) -> str:
        try:
            doc = Document(file)
        except Exception as e:
            raise error_handler.Custom_error(e.args[0])

        binary = ""
        text = ""

        for paragraph in doc.paragraphs:
            text = text + paragraph.text + " "

            for run in paragraph.runs:
                t = run.text
                split = t.strip().split(" ")

                for word in split:
                    word = word.lower()
                    if word in dictionary_of_synonyms:
                        binary += "1"
                    elif word in dictionary_of_zeros:
                        binary += "0"
        # bacon + synonyms
        if (bits == "own1"):
            bacons_patterns = re.findall('.....', binary)
            secret_message = bacon.bacon_pattern_to_string(
                bacons_patterns, bacon.bacons_table)
        elif (bits == "default"):
            secret_message = steganography.binary_to_str(binary)
        return secret_message


# @brief XML elementu přiřadí můj vlastní styl
# @details přiřazený styl značí bit "1"
# @return <w:rStyle w:val="synonym_element"/>
def create_syn_tag() -> str:
    namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    tag = namespace + 'rStyle'
    ns_val = namespace + 'val'
    el = xml.etree.ElementTree.Element(tag)
    el.attrib[ns_val] = "synonym_element"
    return el

# @brief funkce nahrazuje slova na základě hodnoty bitu, který si přeji ukrýt
# @param prop_el element XML interpretace dokumentu
# @param bit jeden bit zprávy
# @param namespace odkaz na registraci XML tagu
# @param word slovo u kterého zjišťuji, zda-li se vyzkytuje ve slovnících (s neslovníkovými slovy nemanipuluji)
# @return vyměněné slovo / nezměněné slovo


def syn_element(prop_el: str, bit: int, namespace: str, word: str, run) -> str:
    syn_word = word
    # na všechny slova, která se vyzkytují ve slovníku přiřadím tag, pouze těmto slovům budu přidělovat bity
    if (word.lower() in dictionary_of_zeros):
        index = list(dictionary_of_zeros.keys()).index(word.lower())

        # jedničkové bity nahradím jejich synonymem
        if bit == '1':
            print("\n", end='')
            print("replacing....")

            # nalezení příslušného synonyma ve druhém slovníku, podle indexu
            syn_word = list(dictionary_of_synonyms.keys())[index]

            print("index in dict: %d (%s)" % (index, word))
            print("syn in dict: %d (%s)" % (index, syn_word))
            print("\n", end='')

        # pokud bylo původní slovo napsané velkými písmeny, nové musí být také
        if (word.isupper()):
            syn_word = syn_word.upper()

        # apply <w:rStyle w:val="synonym"/>
        tag = create_syn_tag()
        prop_el.append(tag)
    elif (word.lower() in dictionary_of_synonyms):
        index = list(dictionary_of_synonyms.keys()).index(word.lower())
        if bit == '0':
            print("\n", end='')
            print("replacing....")

            # nalezení příslušného synonyma ve druhém slovníku, podle indexu
            syn_word = list(dictionary_of_zeros.keys())[index]

            print("index in dict: %d (%s)" % (index, word))
            print("syn in dict: %d (%s)" % (index, syn_word))
            print("\n", end='')

            # pokud bylo původní slovo napsané velkými písmeny, nové musí být také
            if (word.isupper()):
                syn_word = syn_word.upper()

    return syn_word
