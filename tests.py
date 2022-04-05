from codecs import encode
import re
import os
import string
import sys
import timeit
import docx
import matplotlib.pyplot as plt
import numpy as np

#moduly
import bacon
import whitespaces
import xml_parse
import robustness
import synonyms
import steganography
from contextlib import contextmanager


bacon_cover_size = 0
bacon_encoded_size = 0
spaces_cover_size = 0
spaces_encoded_size = 0
syn_cover_size = 0
syn_encoded_size = 0

secret_message = "hromadnytest"
mes_len = len(secret_message)

def encode_all_covers():
    # encode_bacon()
    # encode_spaces()
    encode_syn()
    # encode_own1()
    # encode_own2()


def decode_all_encodes():
    print("\n", end='')
    print("---------------------------------")
    print("DECODING:")
    decode_bacon()
    decode_spaces()
    decode_syn()

def check_robustness(): 
    # bacon_robustness_check()
    # spaces_robustness_check()
    syn_robustness_check()

def calculate_SIR():
    bacon_sir = (bacon_encoded_size-bacon_cover_size)/bacon_cover_size*100
    spaces_sir = (spaces_encoded_size-spaces_cover_size)/spaces_cover_size*100
    syn_sir = (syn_encoded_size-syn_cover_size)/syn_cover_size*100
    print("BACON SIR:\t %f %%" % bacon_sir)
    print("SPACES SIR:\t %f %%" % spaces_sir)
    print("SYNONYMS SIR:\t %f %%" % syn_sir)

def plot_all():
    plot_graphs1()
    plot_graphs2()
    plot_graphs3()
    plot_graphs4()


def plot_graphs1():

    #Přijde vám na některém z těhto souborů něco zvláštního?
    students = [1,2,2,4,4,10]
    cmap = plt.get_cmap('Greys')
    colors = list(cmap(np.linspace(0.45, 0.85, len(students))))
    # Swap in a bright blue for the Lacrosse color.
    colors[5] = 'dodgerblue'
    plt.rcParams.update({'font.size': 22})

    
    wierd = ['Open-space metoda', 'Open-space metoda a metoda synonym','Metoda synonym','Baconova šifra a metoda synonym', 'Baconova šifra', "Žádný"]
    exp = [0.01,0.01,0.01,0.01,0.01,0.01]
    fig1 = plt.figure(figsize=(11, 9))
    patches, texts, autotexts = plt.pie(students, labels = wierd, explode = exp, autopct='%2.1f%%', colors=colors)
    texts[0].set_color('black')
    [autotext.set_color('white') for autotext in autotexts]

    plt.savefig("first.pdf",bbox_inches='tight')

def plot_graphs2():
    #Některý ze souborů je zašifrovaný, dokážete říci který?
    students2 = [1,2,2,4,6,8]
    cmap = plt.get_cmap('Greys')
    colors2 = list(cmap(np.linspace(0.45, 0.85, len(students2))))
    plt.rcParams.update({'font.size': 22})

    # Swap in a bright blue for the Lacrosse color.
    colors2[5] = 'dodgerblue'
    not_changed = ['Open-space metoda', 'Open-space metoda a metoda synonym', 'Baconova šifra a Open-space metoda','Baconova šifra a metoda synonym', 'Metoda synonym', 'Baconova šifra']
    exp2 = [0.01,0.01,0.01,0.01,0.01,0.01]
    fig2 = plt.figure(figsize=(11,9))
    patches2, texts2, autotexts2 = plt.pie(students2, labels = not_changed, explode = exp2, autopct='%2.1f%%', colors=colors2)
    texts2[0].set_color('black')
    [autotext2.set_color('white') for autotext2 in autotexts2]

    plt.savefig("second.pdf",bbox_inches='tight')
 
#vypočítá maximální možnou velikost zprávy, kterou jde do určeného cover textu uložit
def max_secret_message(file, method, file_format): 
    if file_format == "docx": 
        full_text = steganography.print_text(file)
    elif file_format == "txt":
        text_file = open(file)
        full_text = text_file.read()
 
    if method is "synonyms":
        words_available = synonyms.count_dictionary_words(full_text)/8
    elif method is "bacon" or method is "own1" or method is "own2":
        words_available = len(full_text.split())/5
    elif method is "spaces":
        words_available = len(full_text.split())/8

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
    cover_size_path = os.getcwd() + '/cover_files/synonyms'
    path = bytes('/cover_files/synonyms', 'utf-8')

    changed_path = os.path.join(thisdir_bin, b"cover_files")
    changed_path = os.path.join(changed_path, b"synonyms")

    list_of_files = os.listdir(changed_path)

    cnt = 0
    message = 0
    success = 0
    global syn_cover_size
    print("\n", end='')
    print("REPLACING SYNONYMS ENCODING:")
    file_format = ""
    #šifrování všech cover textů pomocí metody synonym
    start = timeit.default_timer()
    for file in list_of_files:
        cnt += 1
        file = os.path.join(changed_path, file)    
        file = str(file, 'UTF-8')

        #zjistím si jméno souboru (poslední soubor v cestě)
        head_tail = os.path.split(file)
        file_name = head_tail[1]
        if file_name.endswith('.txt'):
            file_format = "txt"
        elif file_name.endswith('.docx'):
            file_format = "docx"

        message += max_secret_message(cover_size_path+'/'+file_name, "synonyms", file_format)
        with suppress_stdout():
            check = steganography.main(['-i', file, '-e', '-s', secret_message, '-r'])

        if check is False:
            print("#%d failed ✖ (%s)" % (cnt, file_name))
        else:
            print("#%d encoded 🗸 (%s)" % (cnt, file_name))
            size = os.stat(file)
            syn_cover_size += size.st_size
            success += 1    
    end = timeit.default_timer()
    time = (end - start)
    print("Elapsed time: \t\t%f \t[seconds] " % time)
    print("Cover texts size: \t%d \t[bytes]" % syn_cover_size)
    
    efficiency = time/(float(syn_cover_size)*0.001)
    success_rate = 100*(success/cnt)
    print("Efficiency: \t\t%f \t[time in seconds to encode 1KB]" % efficiency)
    capacity = float(message/syn_cover_size)*100.0
    print("Average capacity: \t%f \t[bits]" % (capacity))

    print("-------------------------------------------------------------------------")
    print("Success rate: \t\t %d/%d 〜 %g%%" % (success,cnt,success_rate))

def encode_own1():
    thisdir_bin = os.getcwdb()
    cover_size_path = os.getcwd() + '/cover_files/synonyms'
    path = bytes('/cover_files/synonyms', 'utf-8')

    changed_path = os.path.join(thisdir_bin, b"cover_files")
    changed_path = os.path.join(changed_path, b"synonyms")

    list_of_files = os.listdir(changed_path)

    cnt = 0
    message = 0
    success = 0
    global syn_cover_size
    syn_cover_size = 0
    file_format = ""
    print("\n", end='')
    print("OWN1 ENCODING (SYN + BACON):")

    #šifrování všech cover textů pomocí metody synonym
    start = timeit.default_timer()
    for file in list_of_files:
        cnt += 1
        file = os.path.join(changed_path, file)    
        file = str(file, 'UTF-8')

        #zjistím si jméno souboru (poslední soubor v cestě)
        head_tail = os.path.split(file)
        file_name = head_tail[1]
        if file_name.endswith('.txt'):
            file_format = "txt"
        elif file_name.endswith('.docx'):
            file_format = "docx"

        message += max_secret_message(cover_size_path+'/'+file_name, "own1", file_format)
        with suppress_stdout():
            check = steganography.main(['-i', file, '-e', '-s', secret_message, '--own1'])

        if check is False:
            print("#%d failed ✖ (%s)" % (cnt, file_name))
        else:
            print("#%d encoded 🗸 (%s)" % (cnt, file_name))
            size = os.stat(file)
            syn_cover_size += size.st_size
            success += 1
    end = timeit.default_timer()
    time = (end - start)
    print("Elapsed time: \t\t%f \t[seconds] " % time)
    print("Cover texts size: \t%d \t[bytes]" % syn_cover_size)
    
    efficiency = time/(float(syn_cover_size)*0.001)
    success_rate = 100*(success/cnt)
    print("Efficiency: \t\t%f \t[time in seconds to encode 1KB]" % efficiency)
    capacity = float(message/syn_cover_size)*100.0
    print("Average capacity: \t%f \t[bits]" % (capacity))

    print("-------------------------------------------------------------------------")
    print("Success rate: \t\t %d/%d 〜 %g%%" % (success,cnt,success_rate))

def encode_own2():
    thisdir_bin = os.getcwdb()
    cover_size_path = os.getcwd() + '/cover_files/synonyms'
    path = bytes('/cover_files/synonyms', 'utf-8')

    changed_path = os.path.join(thisdir_bin, b"cover_files")
    changed_path = os.path.join(changed_path, b"synonyms")

    list_of_files = os.listdir(changed_path)

    cnt = 0
    message = 0
    success = 0
    global syn_cover_size
    syn_cover_size = 0
    print("\n", end='')
    file_format = ""
    print("OWN2 ENCODING (SYN + HUFFMAN):")

    #šifrování všech cover textů pomocí metody synonym
    start = timeit.default_timer()
    for file in list_of_files:
        cnt += 1
        file = os.path.join(changed_path, file)    
        file = str(file, 'UTF-8')

        #zjistím si jméno souboru (poslední soubor v cestě)
        head_tail = os.path.split(file)
        file_name = head_tail[1]
        if file_name.endswith('.txt'):
            file_format = "txt"
        elif file_name.endswith('.docx'):
            file_format = "docx"

        message += max_secret_message(cover_size_path+'/'+file_name, "own2", file_format)
        with suppress_stdout():
            check = steganography.main(['-i', file, '-e', '-s', secret_message, '--own2'])

        if check is False:
            print("#%d failed ✖ (%s)" % (cnt, file_name))
        else:
            print("#%d encoded 🗸 (%s)" % (cnt, file_name))
            size = os.stat(file)
            syn_cover_size += size.st_size
            success += 1
    end = timeit.default_timer()
    time = (end - start)
    print("Elapsed time: \t\t%f \t[seconds] " % time)
    print("Cover texts size: \t%d \t[bytes]" % syn_cover_size)
    
    efficiency = time/(float(syn_cover_size)*0.001)
    success_rate = 100*(success/cnt)
    print("Efficiency: \t\t%f \t[time in seconds to encode 1KB]" % efficiency)
    capacity = float(message/syn_cover_size)*100.0
    print("Average capacity: \t%f \t[bits]" % (capacity))

    print("-------------------------------------------------------------------------")
    print("Success rate: \t\t %d/%d 〜 %g%%" % (success,cnt,success_rate))

def encode_spaces():
    thisdir_bin = os.getcwdb()
    cover_size_path = os.getcwd() + '/cover_files/spaces'
    path = bytes('/cover_files/spaces', 'utf-8')

    changed_path = os.path.join(thisdir_bin, b"cover_files")
    changed_path = os.path.join(changed_path, b"spaces")

    list_of_files = os.listdir(changed_path)

    cnt = 0
    success = 0
    global spaces_cover_size
    print("\n", end='')
    print("ADDING WHITESPACES ENCODING:")
    file_format = ""
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
        if file_name.endswith('.txt'):
            file_format = "txt"
        elif file_name.endswith('.docx'):
            file_format = "docx"

        message += max_secret_message(cover_size_path+'/'+file_name, "spaces",file_format)
        with suppress_stdout():
            check = steganography.main(['-i', file, '-e', '-s', secret_message, '-w'])
        if check is False:
            print("#%d failed ✖ (%s)" % (cnt, file_name))
        else:
            print("#%d encoded 🗸 (%s)" % (cnt, file_name))
            size = os.stat(file)
            spaces_cover_size += size.st_size
            success += 1

    end = timeit.default_timer()
    time = (end - start)
    print("Elapsed time: \t\t%f \t[seconds] " % time)
    size = get_folder_size(cover_size_path)
    print("Cover texts size: \t%d \t[bytes]" % spaces_cover_size)
    
    efficiency = time/(float(spaces_cover_size)*0.001)
    success_rate = 100*(success/cnt)
    print("Efficiency: \t\t%f \t[time in seconds to encode 1KB]" % efficiency)
    capacity = float(message/spaces_cover_size)*100.0
    print("Average capacity: \t%f \t[bits]" % (capacity))
   
    print("-------------------------------------------------------------------------")
    print("Success rate: \t\t %d/%d 〜 %g%%" % (success,cnt,success_rate))

def encode_bacon():
    thisdir_bin = os.getcwdb()
    cover_size_path = os.getcwd() + '/cover_files/bacon'

    changed_path = os.path.join(thisdir_bin, b"cover_files")
    changed_path = os.path.join(changed_path, b"bacon")

    list_of_files = os.listdir(changed_path)

    cnt = 0
    message = 0
    success = 0
    global bacon_cover_size
    print("BACON ENCODING:")
    file_format = ""

    #šifrování všech cover textů pomocí Baconovy šifry
    start = timeit.default_timer()
    for file in list_of_files:
        cnt += 1
        file = os.path.join(changed_path, file)    
        file = str(file, 'UTF-8')
        #zjistím si jméno souboru (poslední soubor v cestě)
        head_tail = os.path.split(file)
        file_name = head_tail[1]
        if file_name.endswith('.txt'):
            file_format = "txt"
        elif file_name.endswith('.docx'):
            file_format = "docx"
    
        message += max_secret_message(cover_size_path+'/'+file_name, "bacon", file_format)
        with suppress_stdout():
            check = steganography.main(['-i', file, '-e', '-s', secret_message, '-b'])
     

        if check is False:
            print("#%d failed ✖ (%s)" % (cnt, file_name))
        else:
            print("#%d encoded 🗸 (%s)" % (cnt, file_name))
            size = os.stat(file)
            bacon_cover_size += size.st_size
            success += 1
    size = get_folder_size(cover_size_path)

    end = timeit.default_timer()
    time = (end - start)
    print("Elapsed time: \t\t%f \t[seconds] " % time)
    print("Cover texts size: \t%d \t[bytes]" % bacon_cover_size)
    
    efficiency = time/(float(bacon_cover_size)*0.001)
    success_rate = 100*(success/cnt)
    print("Efficiency: \t\t%f \t[time in seconds to encode 1KB]" % efficiency)
    capacity = float(message/bacon_cover_size)*100.0
    print("Average capacity: \t%f \t[bits]" % (capacity))
  
    print("-------------------------------------------------------------------------")
    print("Success rate: \t\t %d/%d 〜 %g%%" % (success,cnt,success_rate))


def decode_bacon():
    thisdir_bin = os.getcwdb()
    changed_path = os.path.join(thisdir_bin, b"encoded")

    list_of_files = os.listdir(changed_path)
    bacon_files = []
    encoded_path = os.getcwd()

    cnt = 0
    message = 0
    success = 0
    global bacon_encoded_size
    print("BACON DECODING:")
    for file in list_of_files:
        file = str(file, 'UTF-8')
     

        if file.startswith("bacon"):
            bacon_files.append(file)
            size = os.stat(encoded_path + "/encoded/" + file)
            bacon_encoded_size += size.st_size
       
    for encoded in bacon_files:
        robustness.change_font_style("encoded/" + encoded)
        cnt += 1
        with suppress_stdout():
            check = steganography.main(['-i', "encoded/" + encoded, '-d', '-s', '-b'])
            head_tail = os.path.split(encoded)
            file_name = head_tail[1]

    bacon_decodes = []
    decoded_path = os.path.join(thisdir_bin, b"decoded")
    list_of_decoded = os.listdir(decoded_path)

    #porovnání, jestli zpráva zůstala celá neporušená
    for file in list_of_decoded:
        file = str(file, 'UTF-8')
        if file.startswith("bacon"):
            bacon_decodes.append(file)

    cnt = 0
    success = 0
    failed = 0
    for decoded in bacon_decodes:
        cnt += 1
        text = steganography.print_text("decoded/"+decoded)
        text = text[0:mes_len]
        #zpráva zůstala zachována
        if text.lower() == secret_message.lower():
            success += 1
        else:
            failed += 1

    #úspěšně se zachovaly všechny zprávy
    if failed == 0:
        print("All messages DECODED SUCCESSFULLY!")
        print("\n", end='')
    else:
        print("DECODED %d/%d" % (success,cnt))
        print("\n", end='')

def decode_spaces():
    thisdir_bin = os.getcwdb()
    changed_path = os.path.join(thisdir_bin, b"encoded")

    list_of_files = os.listdir(changed_path)
    spaces_files = []
    encoded_path = os.getcwd()

    cnt = 0
    message = 0
    success = 0
    global spaces_encoded_size
    print("SPACES DECODING:")
    for file in list_of_files:
        file = str(file, 'UTF-8')
     

        if file.startswith("spaces"):
            spaces_files.append(file)
            size = os.stat(encoded_path + "/encoded/" + file)
            spaces_encoded_size += size.st_size
       
    for encoded in spaces_files:
        with suppress_stdout():
            check = steganography.main(['-i', "encoded/" + encoded, '-d', '-s', '-w'])
            head_tail = os.path.split(encoded)
            file_name = head_tail[1]
            
        # if check is False:
        #     print("#%d failed ✖ (%s)" % (cnt, file_name))
        # else:
        #     print("#%d decoded 🗸 (%s)" % (cnt, file_name))

    spaces_decodes = []
    decoded_path = os.path.join(thisdir_bin, b"decoded")
    list_of_decoded = os.listdir(decoded_path)

    #porovnání, jestli zpráva zůstala celá neporušená
    for file in list_of_decoded:
        file = str(file, 'UTF-8')
        if file.startswith("spaces"):
            spaces_decodes.append(file)

    cnt = 0
    success = 0
    failed = 0
    for decoded in spaces_decodes:
        cnt += 1
        text = steganography.print_text("decoded/"+decoded)
        text = text[0:mes_len]

        #zpráva zůstala zachována
        if text.lower() == secret_message.lower():
            success += 1
        else:
            failed += 1

    #úspěšně se zachovaly všechny zprávy
    if failed == 0:
        print("All messages DECODED SUCCESSFULLY!")
        print("\n", end='')
    else:
        print("DECODED %d/%d" % (success,cnt))
        print("\n", end='')

def decode_syn():
    thisdir_bin = os.getcwdb()
    changed_path = os.path.join(thisdir_bin, b"encoded")

    list_of_files = os.listdir(changed_path)
    syn_files = []
    encoded_path = os.getcwd()

    cnt = 0
    message = 0
    success = 0
    global syn_encoded_size
    print("SYNONYMS DECODING:")
    for file in list_of_files:
        file = str(file, 'UTF-8')
     

        if file.startswith("synonyms"):
            syn_files.append(file)
            size = os.stat(encoded_path + "/encoded/" + file)
            syn_encoded_size += size.st_size
       
    for encoded in syn_files:
        with suppress_stdout():
            check = steganography.main(['-i', "encoded/" + encoded, '-d', '-s', '-r'])
            head_tail = os.path.split(encoded)
            file_name = head_tail[1]
            
        # if check is False:
        #     print("#%d failed ✖ (%s)" % (cnt, file_name))
        # else:
        #     print("#%d decoded 🗸 (%s)" % (cnt, file_name))

    syn_decodes = []
    decoded_path = os.path.join(thisdir_bin, b"decoded")
    list_of_decoded = os.listdir(decoded_path)

    # #porovnání, jestli zpráva zůstala celá neporušená
    for file in list_of_decoded:
        file = str(file, 'UTF-8')
        if file.startswith("synonyms"):
            syn_decodes.append(file)

    cnt = 0
    success = 0
    failed = 0
    for decoded in syn_decodes:
        cnt += 1
        text = steganography.print_text("decoded/"+decoded)
        text = text[0:mes_len]

        #zpráva zůstala zachována
        if text.lower() == secret_message.lower():
            success += 1
        else:
            failed += 1

    #úspěšně se zachovaly všechny zprávy
    if failed == 0:
        print("All messages DECODED SUCCESSFULLY!")
        print("\n", end='')
    else:
        print("DECODED %d/%d" % (success,cnt))
        print("\n", end='')

    
def bacon_robustness_check():
    thisdir_bin = os.getcwdb()
    changed_path = os.path.join(thisdir_bin, b"encoded")
    robustness_path = os.path.join(thisdir_bin, b"robustness")

    list_of_files = os.listdir(changed_path)
    bacon_changed_files = []
    changed_files = []
    bacon_files = []
    list_of_changed_styles = os.listdir(robustness_path)

    encoded_path = os.getcwd()

    print("BACON ROBBUSTNESS CHECK:")
    for file in list_of_files:
        file = str(file, 'UTF-8')
     
        if file.startswith("bacon"):
            bacon_files.append(file)

    #změna formátování
    for encoded in bacon_files:
        robustness.change_font_style("encoded/" + encoded)

    #vyberu pouze souboru pro tuto metodu
    for changed in list_of_changed_styles:
        file = str(changed, 'UTF-8')
        if file.startswith("bacon"):
            bacon_changed_files.append(file)

    decoded_path = os.path.join(thisdir_bin, b"decoded")
    list_of_decoded = os.listdir(decoded_path)

    cnt = 0
    success = 0
    failed = 0
    if bacon_changed_files:
        for bacon_chnaged in bacon_changed_files:
            cnt += 1
            #dekodování souboru se změněným stylem
            with suppress_stdout():
                steganography.main(['-i', "robustness/" + bacon_chnaged, '-d', '-s', '-b'])
                text = steganography.print_text("robustness/"+bacon_chnaged)

            #ořezání zprávy
            text = text[0:mes_len]
            #zpráva zůstala zachována
            if text.lower() == secret_message.lower():
                success += 1
                print(text.lower())

            else:
                failed += 1

        #úspěšně se zachovaly všechny zprávy
        if failed == 0:
            print("After ALL FORMAT CHANGES all messages DECODED SUCCESSFULLY!")
            print("\n", end='')
        else:
            print("After ALL FORMAT CHANGES %d/%d messages sucesfully decoded" % (success,cnt))
            print("\n", end='')
    else:
        print("After ALL FORMAT CHANGES NO messages decoded!")
        print("\n", end='')



def spaces_robustness_check():
    thisdir_bin = os.getcwdb()
    changed_path = os.path.join(thisdir_bin, b"encoded")
    robustness_path = os.path.join(thisdir_bin, b"robustness")

    list_of_files = os.listdir(changed_path)
    spaces_changed_files = []
    spaces_files = []
    list_of_changed_styles = os.listdir(robustness_path)


    print("SPACES ROBBUSTNESS CHECK:")
    for file in list_of_files:
        file = str(file, 'UTF-8')
     
        if file.startswith("spaces"):
            spaces_files.append(file)

    #změna formátování
    print(spaces_files)
    for encoded in spaces_files:
        robustness.change_font_style("encoded/" + encoded)

    #vyberu pouze souboru pro tuto metodu
    for changed in list_of_changed_styles:
        file = str(changed, 'UTF-8')
        if file.startswith("spaces"):
            spaces_changed_files.append(file)

    decoded_path = os.path.join(thisdir_bin, b"decoded")
    list_of_decoded = os.listdir(decoded_path)

    cnt = 0
    success = 0
    failed = 0
    if spaces_changed_files:
        for spaces_chnaged in spaces_changed_files:
            cnt += 1

            #dekodování souboru se změněným stylem
            with suppress_stdout():
                steganography.main(['-i', "robustness/" + spaces_chnaged, '-d', '-s', '-w'])
                text = steganography.print_text("robustness/"+ spaces_chnaged)

            #ořezání zprávy
            text = text[0:mes_len]
            #zpráva zůstala zachována
            if text.lower() == secret_message.lower():
                success += 1
                print(text.lower())

            else:
                failed += 1

        #úspěšně se zachovaly všechny zprávy
        if failed == 0:
            print("After ALL FORMAT CHANGES all messages DECODED SUCCESSFULLY!")
            print("\n", end='')
        else:
            print("After ALL FORMAT CHANGES %d/%d messages sucesfully decoded" % (success,cnt))
            print("\n", end='')
    else:
        print("After ALL FORMAT CHANGES NO messages decoded!")
        print("\n", end='')


def syn_robustness_check():
    thisdir_bin = os.getcwdb()
    changed_path = os.path.join(thisdir_bin, b"encoded")
    robustness_path = os.path.join(thisdir_bin, b"robustness")

    list_of_files = os.listdir(changed_path)
    syn_changed_files = []
    syn_files = []
    list_of_changed_styles = os.listdir(robustness_path)


    print("SYNONYMS ROBBUSTNESS CHECK:")
    for file in list_of_files:
        file = str(file, 'UTF-8')
     
        if file.startswith("syn"):
            syn_files.append(file)

    #změna formátování
    for encoded in syn_files:
        robustness.change_font_style("encoded/" + encoded)

    #vyberu pouze souboru pro tuto metodu
    print(list_of_changed_styles)
    for changed in list_of_changed_styles:
        file = str(changed, 'UTF-8')
        if file.startswith("syn"):
            syn_changed_files.append(file)

    # decoded_path = os.path.join(thisdir_bin, b"decoded")

    # cnt = 0
    # success = 0
    # failed = 0
    # for syn_chnaged in syn_changed_files:
    #     cnt += 1

    #     #dekodování souboru se změněným stylem
   
    #     steganography.main(['-i', "robustness/" + syn_chnaged, '-d', '-s', '-r'])
    #     text = steganography.print_text("robustness/"+ syn_chnaged)

    #     #ořezání zprávy
    #     text = text[0:mes_len]
    #     #zpráva zůstala zachována
    #     if text.lower() == secret_message.lower():
    #         success += 1
    #         print(text.lower())

    #     else:
    #         failed += 1

    # #úspěšně se zachovaly všechny zprávy
    # if failed == 0:
    #     print("After ALL FORMAT CHANGES all messages DECODED SUCCESSFULLY!")
    #     print("\n", end='')
    # else:
    #     print("After ALL FORMAT CHANGES %d/%d messages sucesfully decoded" % (success,cnt))
    #     print("\n", end='')

def plot_graphs3():
    #metoda synonym
    y = [0.0065,0.023,0.017,0.021]
    x = [12,40,80,120]

    #baconova šifra
    y2 = [0.005,0.021,0.018,0.026]

    #open-space
    y3 = [0.007,0.036,0.032,0.035]
    fig3 = plt.figure(figsize=(11,9))

    plt.plot(x,y)
    plt.plot(x,y2)
    plt.plot(x,y3)
    plt.title("Efektivita jednotlivých metod")
    plt.ylabel("Čas potřebný k zašifrování 1kB dat [s]")
    plt.xlabel("Velikost cover souboru [kB]")

    ax = plt.gca()
    ax.legend(['Metoda synonym', 'Baconova šifra', 'Ope-space'])

    plt.savefig("effectivness.pdf",bbox_inches='tight')


def plot_graphs4():
    #metoda synonym
    y = [0.0065,0.023,0.017,0.021]
    x = [12,40,80,120]

    #baconova šifra
    y2 = [0.012,0.022,0.018,0.022]

    #open-space
    y3 = [0.009,0.02,0.019,0.023]
    fig4 = plt.figure(figsize=(11,9))

    plt.plot(x,y)
    plt.plot(x,y2)
    plt.plot(x,y3)
    plt.title("Efektivita jednotlivých metod")
    plt.ylabel("Čas potřebný k zašifrování 1kB dat [s]")
    plt.xlabel("Velikost cover souboru [kB]")

    ax = plt.gca()
    ax.legend(['Metoda synonym', 'Metoda synonym + Baconovo šifrování', 'Metoda synonym + Huffmanovo kódování'])

    plt.savefig("own_methods_comparison.pdf",bbox_inches='tight')


if __name__ == "__main__":
    encode_all_covers()
    # decode_all_encodes()
    check_robustness()

    # calculate_SIR()
    # plot_all()