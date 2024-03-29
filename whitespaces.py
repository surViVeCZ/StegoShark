# ----------------------------------------------------------------------
# Autor:          Petr Pouč
# Login:          xpoucp01
# Datum:          27.04.2022
# Název práce:    Digitální textová steganografie
# Cíl práce:      Implementace 4 vybraných steganografických metod
# ----------------------------------------------------------------------

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from termcolor import colored
import xml.etree.ElementTree
import xml.dom.minidom
import error_handler
import steganography
import xml_parse

# @brief počítá počet mezer v textu
# @param text textová část souboru
# @return počet mezer
# @note funkce je nezbytná, pro určení, zda-li má text dostatečnou kapacitu na ukrytí tajné zprávy


def count_spaces(text: str) -> int:
    cnt = 0
    for ch in text:
        if ch == " ":
            cnt += 1
    return cnt


class spaces_cipher:
    def __init__(self, file: str, message: str):
        self.file = file
        self.message = message
    # @brief ukrytí tajné zprávy pomocí Open-space metody
    # @param file vstupní cover soubor
    # @param message tajná zpráva, kterou si přejeme ukrýt
    # @return cesta k zašifrovanému souboru

    def Spaces_encode(self, file: str, message: str) -> str:
        print("INSIDE ENCODE")
        binary_mes = steganography.str_to_binary(message)
        print(binary_mes)
        print("\n", end='')

        # nutno zjistit počet slov, více slov umožňuje ukrytí delší zprávy
        full_text = steganography.print_text(file)

        full_text.split()
        number_of_spaces = count_spaces(full_text)

        # pro ukrytí jednoho znaku je potřeba 8 znaků cover textu
        if (len(message*8) > number_of_spaces):
            print("Cover text doesn't have enough capacity to hide this message")
            return False

        split_obj = xml_parse.XML_split(binary_mes, file, "spaces", "default")
        path = split_obj.split_document()
        return path

    # @brief dešifrování pomocí Open-space metody
    # @param file zašifrovaný soubor
    # @return tajná zpráva
    # @note správně dešifrovat můžeme pouze soubory zašifrované stejnou metodou
    def Spaces_decode(self, file: str) -> str:
        try:
            doc = Document(file)
        except Exception as e:
            raise error_handler.Custom_error(e.args[0])

        doc.styles
        binary = ""
        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                if run.style.name == "spaces_style":
                    binary = binary + '1'
                elif run.text == " ":
                    binary = binary + '0'

        secret_message = steganography.binary_to_str(binary)
        return secret_message


# @brief nastavení mezery na určitou hodnotu
# @return XML element se změněnou hodnotou mezery
# @note hodnota mezery odpovídá fontu velikosti 9,5
def create_whitespace_el() -> str:
    namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    tag = namespace + 'sz'
    ns_val = namespace + 'val'
    el = xml.etree.ElementTree.Element(tag)
    el.attrib[ns_val] = "19"  # hodnota mezery odpovídá fontu velikosti 9,5
    return el

# @brief XML elementu přiřadí můj vlastní styl
# @details přiřazený styl značí bit "1"
# @return <w:rStyle w:val="spaces_style"/>
# @note styl slouží pouze jako tag indikující jedničkový bit, neobsahuje žádné vlastnosti


def create_tag() -> str:
    namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    tag = namespace + 'rStyle'
    ns_val = namespace + 'val'
    el = xml.etree.ElementTree.Element(tag)
    el.attrib[ns_val] = "spaces_style"
    return el

# @brief nahraje styl do elementu, který má bit = 1
# @param prop_el element XML interpretace dokumentu
# @param bit 1 bit zprávy
# @param namespace odkaz na registraci XML tagu


def spaces_element(prop_el: str, bit: int, namespace: str) -> None:
    if bit == "1":
        for subelement in prop_el[:]:
            if (subelement.tag == namespace + "sz"):
                prop_el.remove(subelement)
        style_el = create_whitespace_el()
        style_tag = create_tag()
        prop_el.append(style_tag)
        prop_el.append(style_el)


# @brief do dokumentu docx se nahraje můj vlastní styl, který později použiji pro ukrytí zprávy
# @param font_styles základní styly dokumentu .docx
# @note abych mohl v XML přiřazovat elementům můj vlastní styl, musí nejprve tento styl v dokumentu existovat
def add_spaces_style(font_styles: str) -> None:
    # check jestli styl již existuje, nelze přidat 2x
    custom_style_present = False
    for style in font_styles:
        if 'spaces_style' == style.name:
            custom_style_present = True
    # nastavení custom stylu
    if not custom_style_present:
        font_charstyle = font_styles.add_style(
            'spaces_style', WD_STYLE_TYPE.CHARACTER)
