# -*- coding: utf-8 -*-


#----------------------------------------------------------------------
# Autor:          Petr Pouč                                           
# Login:          xpoucp01
# Datum:          27.04.2022
# Název práce:    Digitální textová steganografie 
# Cíl práce:      Implementace 4 vybraných steganografických metod
#----------------------------------------------------------------------
import os
from base64 import encode
from cProfile import label
import sys
import tkinter as tk
from tkinter import LEFT, RIDGE, RIGHT, Button, Entry, filedialog, Text, Label
from tkinter import ttk
from tkinter import messagebox
import os
from tkinter.messagebox import showinfo

from steganography import main
import bacon
import whitespaces
import synonyms
import huffman_coding
import error_handler

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

text_path = None
## @brief zjistí zvolenou metodu v combo box
def method_changed(event):
    global method
    method = combo.current()
    
## @brief volba vstupního souboru
def choose_input():
    global text_path
    global filepath
    try:
        inputfile = filedialog.askopenfile(initialdir="/", title="Zvol soubor k zašifrování",filetypes=(("documents", "*.docx"), ("text files", "*.txt")))
    except Exception as e:
        raise error_handler.Custom_error(e.args[0])
    if inputfile:
        filepath = os.path.abspath(inputfile.name)

    head_tail = os.path.split(filepath)
    text_path.configure(text=head_tail[1])
        
## @brief vložení tajné zprávy do vstupního souboru na základě zvolené steganografické metody
def encode():
    global method
    method_name = ""
    secret_mes = message.get('1.0', 'end-1c')
    try:
        print('Message index is: {}\n'.format(method),  end = '')
    except:
        raise Exception(messagebox.showerror("Error", "Je potřeba vybrat steganografickou metodu."))

    print("Secret message is: " + secret_mes)
    try:
        str(filepath)
    except:
        raise Exception(messagebox.showerror("Error", "Musíš zvolit vstupní soubor."))
    if method == 0:
        method_name = '-b'
    elif method == 1:
        method_name = '-w'
    elif method == 2:
        method_name = '-r'
    elif method == 3:
        method_name = '--own1'
    elif method == 4:
        method_name = '--own2'
    
    try:
        check = main(['-i', str(filepath), '-e', '-s', secret_mes, method_name])
    except:
        raise Exception(messagebox.showerror("ERROR!", "Chybně zadané parametry! (Baconova šifra beze pouze znaky A-Z (bez mezer a speciálních znaků), totéž platí pro metodu synonym vužívající tohoto šifrování"))
    if check is False:
        messagebox.showerror("ERROR!", "Soubor nemá dostatečnou kapacitu na ukrytí této zprávy.")
    else:
        messagebox.showinfo("ENCODED!", "Zpráva byla úspěšně zašifrována do zvoleného souboru!")
    message.delete(1.0,"end")

## @brief dešifrování zvoleného souboru zvolenou metodou
#@note soubor musí být dešifrován metodou, kterou byl zašifrován
def decode():
    global method
    global message
    method_name = ""
    try:
        print('Message index is: {}\n'.format(method),  end = '')
    except:
        raise Exception(messagebox.showerror("Error", "Je potřeba vybrat steganografickou metodu."))
    try:
        str(filepath)
    except:
        raise Exception(messagebox.showerror("Error", "Nutno zlovit vstupní soubor."))
        
    bacon_obj = bacon.bacon_cipher(filepath,message)
    syn_obj = synonyms.syn_cipher(filepath,message)
    spaces_obj = whitespaces.spaces_cipher(filepath,message)
    
    # print(f'Method is: {method}')
    # print(f'filepath is: {str(filepath)}')
    if method == 0:
        secret = bacon_obj.Bacon_decode(str(filepath))
    elif method == 1:
         secret = spaces_obj.Spaces_decode(str(filepath))
    elif method == 2:
        secret = syn_obj.syn_decode(str(filepath), "default")
    elif method == 3:
        secret = syn_obj.syn_decode(str(filepath), "own1")
    elif method == 4:
        try:
            secret = syn_obj.syn_decode(str(filepath), "own2")
        except:
            raise Exception(messagebox.showerror("ERROR!", "Dešifrování Huffmanova kódování nebylo implementováno. Huffmanův strom musí být vložen do textu, nebo domluven mezi komunikujícími stranami předem."))

    print(f'SECRET IS: {secret}')
    #text = steganography.print_text(str(filepath))
    message.delete(1.0,"end")
    message.insert('1.0', secret)
    messagebox.showinfo("DECODED!", "Soubor byl dešifrován")

root = tk.Tk()
root.geometry("640x500")
root.maxsize(640,500)
root.minsize(640,500)
root.configure(background='#DCDFE0')

heading = Label(text="STEGOSHARK 2000", bg="black", fg="white", height="3", width="800")
heading.pack()

l1 = Label(text = "Vstupní soubor:", background="#DCDFE0")
l1.place(x = 20, y = 90)
#input file button
open_file = tk.Button(root, text = "Vybrat vstupní soubor", padx=5,pady=5, bg="#4173EA", fg="#FFFFFF", 
            activebackground="#1C3A83", activeforeground="#FFFFFF", command=choose_input)
open_file.place(x = 140, y = 80)

l2 = Label(text = "Vlož tajnou zprávu, kterou si přeješ ukrýt:", background="#DCDFE0")
l2.place(x = 20, y = 140)


#entry secret message
message = Text(root, bg="white", height="5", width="60")
message.place(x = 20, y = 170)

text_path = Label(text = " ", background="#DCDFE0", foreground="#8B9092")
text_path.place(x = 320, y = 90)

#encode button
encode_button = Button(root, text="ŠIFROVAT", command=encode, padx=85, bg="#4173EA", fg="#FFFFFF", activebackground="#1C3A83", activeforeground="#FFFFFF")
encode_button.place(x = 60, y = 450)

decode_button = Button(root, text="DEŠIFROVAT", command=decode, padx=85, bg="#4173EA", fg="#FFFFFF", activebackground="#1C3A83", activeforeground="#FFFFFF")
decode_button.place(x = 330, y = 450)


selected_method = tk.StringVar()
combo = ttk.Combobox(root,textvariable=selected_method, width=35)
combo['values'] = ["Baconova šifra", "Open-space metoda", "Metoda synonym", "Metoda synonym s baconovým šifrováním", "Huffmanovo kódování"]
combo['state'] = 'readonly'
combo.set('---')
combo.place(x = 20, y = 300)
combo.bind('<<ComboboxSelected>>', method_changed)

root.mainloop()