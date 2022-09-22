# ----------------------------------------------------------------------
# Autor:          Petr Pouč
# Login:          xpoucp01
# Datum:          27.04.2022
# Název práce:    Digitální textová steganografie
# Cíl práce:      Implementace 4 vybraných steganografických metod
# ----------------------------------------------------------------------


# Šifrování pomocí Huffmanova kódování jsem dne 30.03.2022 převzal z této stránky
# cite https://www.programiz.com/dsa/huffman-coding

from email import message
import string
import collections
from typing import Dict
from typing import List


# @brief vytvoření uzlů stromu
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    # @brief dítě uzlu
    def children(self):
        return (self.left, self.right)

    # @brief uzel stromu
    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


# @brief funkce generuje Huffmanův strom
# @cite https://www.programiz.com/dsa/huffman-coding
# @param node uzel stromu
# @param left parametr určuje, kterou cestou se vydáme
# @param binString binární vzor pro jednotlivý znak
# @note funkce je rekurzivně volána, dokud není vyvtořen celý strom
def huffman_code_tree(node, left=True, binString='') -> dict:
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    tree = dict()
    tree.update(huffman_code_tree(l, True, binString + '0'))
    tree.update(huffman_code_tree(r, False, binString + '1'))
    return tree


# @brief zjistí frekvenci jednotlivých znaků v textu
# @details znakům následně přiřadí vzor a zprávu převede do Huffmanova kódu
# @cite https://www.programiz.com/dsa/huffman-coding
# @param message vstupní tajná zpráva
# @return zpráva převedená do Huffmanova kódu
def get_frequency(message: str) -> str:
    freq = {}
    huffman_message = ""
    for c in message:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    nodes = freq

    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))

        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    huffmanCode = huffman_code_tree(nodes[0][0])

    print(' Char | Huffman code ')
    print('----------------------')
    for (char, frequency) in freq:
        print(' %-4r |%12s' % (char, huffmanCode[char]))

    for character in message:
        huffman_message += huffmanCode[character]

    # tajná zprává převedena pomocí huffmanova kódování na úspornější řetězec
    return huffman_message
