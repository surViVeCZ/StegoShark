import re
import os
import string
import sys

import docx

#moduly
import bacon
import whitespaces
import xml_parse
import synonyms
import steganography


def encode_all_covers():
    # encode_bacon()
    # encode_spaces()
    encode_syn()
 
 
def encode_syn():
    thisdir = os.getcwdb()
    path = bytes('/cover_files/synonyms', 'utf-8')

    changed_path = os.path.join(thisdir, b"cover_files")
    changed_path = os.path.join(changed_path, b"synonyms")
    print(changed_path)

    list_of_files = os.listdir(changed_path)

    for file in list_of_files:
        file = os.path.join(changed_path, file)    
        file = str(file, 'UTF-8')
        # synonyms.syn_encode(file, "hromadnytestik")
        # doc = docx.Document('cover_files/synonyms/old_man_and_the_sea.docx')
        steganography.main(['-i', file, '-e', '-s', 'x', '-r'])

if __name__ == "__main__":
    encode_all_covers()