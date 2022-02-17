import re
import os
import string

def encode_all_covers():
    thisdir = os.getcwd()
# r=root, d=directories, f = files
    for r, d, f in os.walk(thisdir):
        for file in f:
            if file.endswith(".docx"):
                print(os.path.join(r, file))

if __name__ == "__main__":
    encode_all_covers()