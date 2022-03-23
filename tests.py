import re
import os
import string
import sys
import timeit
import docx

#moduly
import bacon
import whitespaces
import xml_parse
import synonyms
import steganography
from contextlib import contextmanager


def encode_all_covers():
    encode_bacon()
    encode_spaces()
    encode_syn()
 
#vypočítá maximální možnou velikost zprávy, kterou jde do určeného cover textu uložit
def max_secret_message(file, method):
    message = "abcd"
    
    full_text = steganography.print_text(file)
    if method is "synonyms":
        words_available = synonyms.count_dictionary_words(full_text)
    elif method is "bacon":
        words_available = len(re.findall(r'\w+', full_text))
    elif method is "spaces":
        words_available = len(re.findall(r'\w+', full_text))

    return words_available

#cite: https://stackoverflow.com/questions/2125702/how-to-suppress-console-output-in-python
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout


def get_folder_size(full_path):
    size = 0
    for path, dirs, files in os.walk(full_path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    return size


 
def encode_syn():
    thisdir_bin = os.getcwdb()
    size_path = os.getcwd() + '/cover_files/synonyms'
    path = bytes('/cover_files/synonyms', 'utf-8')

    changed_path = os.path.join(thisdir_bin, b"cover_files")
    changed_path = os.path.join(changed_path, b"synonyms")

    list_of_files = os.listdir(changed_path)

    cnt = 0
    message = 0
    success = 0
    print("\n", end='')
    print("REPLACING SYNONYMS ENCODING:")

    #šifrování všech cover textů pomocí metody synonym
    start = timeit.default_timer()
    for file in list_of_files:
        cnt += 1
        file = os.path.join(changed_path, file)    
        file = str(file, 'UTF-8')

        #zjistím si jméno souboru (poslední soubor v cestě)
        head_tail = os.path.split(file)
        file_name = head_tail[1]

        message += max_secret_message(size_path+'/'+file_name, "synonyms")
        with suppress_stdout():
            check = steganography.main(['-i', file, '-e', '-s', 'hromadnytest', '-r'])

        if check is False:
            print("#%d failed ✖ (%s)" % (cnt, file_name))
        else:
            print("#%d encoded 🗸 (%s)" % (cnt, file_name))
            success += 1
    end = timeit.default_timer()
    time = (end - start)
    print("Elapsed time: \t\t%f \t[seconds] " % time)
    size = get_folder_size(size_path)
    print("Cover texts size: \t%d \t[bytes]" % size)
    
    efficiency = time/(float(size)*0.001)
    success_rate = 100*(success/cnt)
    print("Efficiency: \t\t%f \t[time in seconds to encode 1KB]" % efficiency)
    print("Average capacity: \t%d \t\t[bits]" % (message/cnt))

    print("-------------------------------------------------------------------------")
    print("Success rate: \t\t %d/%d 〜 %g%%" % (success,cnt,success_rate))

def encode_spaces():
    thisdir_bin = os.getcwdb()
    size_path = os.getcwd() + '/cover_files/spaces'
    path = bytes('/cover_files/spaces', 'utf-8')

    changed_path = os.path.join(thisdir_bin, b"cover_files")
    changed_path = os.path.join(changed_path, b"spaces")

    list_of_files = os.listdir(changed_path)

    cnt = 0
    success = 0
    print("\n", end='')
    print("ADDING WHITESPACES ENCODING:")

     #šifrování všech cover textů pomocí vkládání mezislovních mezer
    message = 0
    start = timeit.default_timer()
    for file in list_of_files:
        cnt += 1
        file = os.path.join(changed_path, file)    
        file = str(file, 'UTF-8')

        #zjistím si jméno souboru (poslední soubor v cestě)
        head_tail = os.path.split(file)
        file_name = head_tail[1]

        message += max_secret_message(size_path+'/'+file_name, "spaces")
        with suppress_stdout():
            check = steganography.main(['-i', file, '-e', '-s', 'hromadnytest', '-w'])
        if check is False:
            print("#%d failed ✖ (%s)" % (cnt, file_name))
        else:
            print("#%d encoded 🗸 (%s)" % (cnt, file_name))
            success += 1

    end = timeit.default_timer()
    time = (end - start)
    print("Elapsed time: \t\t%f \t[seconds] " % time)
    size = get_folder_size(size_path)
    print("Cover texts size: \t%d \t[bytes]" % size)
    
    efficiency = time/(float(size)*0.001)
    success_rate = 100*(success/cnt)
    print("Efficiency: \t\t%f \t[time in seconds to encode 1KB]" % efficiency)
    print("Average capacity: \t%d \t\t[bits]" % (message/cnt))
   
    print("-------------------------------------------------------------------------")
    print("Success rate: \t\t %d/%d 〜 %g%%" % (success,cnt,success_rate))

def encode_bacon():
    thisdir_bin = os.getcwdb()
    size_path = os.getcwd() + '/cover_files/bacon'
    path = bytes('/cover_files/bacon', 'utf-8')

    changed_path = os.path.join(thisdir_bin, b"cover_files")
    changed_path = os.path.join(changed_path, b"bacon")

    list_of_files = os.listdir(changed_path)

    cnt = 0
    message = 0
    success = 0
    print("BACON ENCODING:")

    #šifrování všech cover textů pomocí Baconovy šifry
    start = timeit.default_timer()
    for file in list_of_files:
        cnt += 1
        file = os.path.join(changed_path, file)    
        file = str(file, 'UTF-8')

        #zjistím si jméno souboru (poslední soubor v cestě)
        head_tail = os.path.split(file)
        file_name = head_tail[1]
    
        message += max_secret_message(size_path+'/'+file_name, "bacon")
        with suppress_stdout():
            check = steganography.main(['-i', file, '-e', '-s', 'hromadnytest', '-b'])

        if check is False:
            print("#%d failed ✖ (%s)" % (cnt, file_name))
        else:
            print("#%d encoded 🗸 (%s)" % (cnt, file_name))
            success += 1
    size = get_folder_size(size_path)

    end = timeit.default_timer()
    time = (end - start)
    print("Elapsed time: \t\t%f \t[seconds] " % time)
    size = get_folder_size(size_path)
    print("Cover texts size: \t%d \t[bytes]" % size)
    
    efficiency = time/(float(size)*0.001)
    success_rate = 100*(success/cnt)
    print("Efficiency: \t\t%f \t[time in seconds to encode 1KB]" % efficiency)
    print("Average capacity: \t%d \t\t[bits]" % (message/cnt))
  
    print("-------------------------------------------------------------------------")
    print("Success rate: \t\t %d/%d 〜 %g%%" % (success,cnt,success_rate))

if __name__ == "__main__":
    encode_all_covers()