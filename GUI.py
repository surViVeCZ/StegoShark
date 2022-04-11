from base64 import encode
from cProfile import label
import sys
import tkinter as tk
from tkinter import LEFT, RIDGE, RIGHT, Button, Entry, filedialog, Text, Label
from tkinter import ttk
import os
from tkinter.messagebox import showinfo

from matplotlib.pyplot import text

def month_changed(event):
    method = selected_method.get()
    print("You selected: " + method)
    # showinfo(
    #     title='Result',
    #     message=f'You selected {selected_method.get()}!'
    # )

def choose_input():
    inputfile = filedialog.askopenfile(initialdir="/", title="Select file to encode",
    filetypes=(("documents", "*.docx"), ("text files", "*.txt")))

def encode():
    secret_mes = message.get('1.0', 'end-1c')
    print("Secret message: " + secret_mes)

root = tk.Tk()
root.geometry("640x500")
root.configure(background='#DCDFE0')
# Steganography tool for text encoding and decoding
heading = Label(text="STEGOSHARK 2000 ^^", bg="black", fg="white", height="3", width="800")
heading.pack()

l1 = Label(text = "Input file:", background="#DCDFE0")
l1.place(x = 20, y = 90)
#input file button
open_file = tk.Button(root, text = "Choose input file", padx=5,pady=5, bg="#4173EA", fg="#FFFFFF", 
            activebackground="#1C3A83", activeforeground="#FFFFFF", command=choose_input)
open_file.place(x = 120, y = 80)




l2 = Label(text = "Insert secret message you want to hide:", background="#DCDFE0")
l2.place(x = 20, y = 140)

#entry secret message
message = Text(root, bg="white", height="5", width="60")
message.place(x = 20, y = 170)

#encode button
encode_button = Button(root, text="ENCODE", command=encode, padx=85, pady=1)
encode_button.place(x = 70, y = 450)

decode_button = Button(root, text="DECODE", command=encode, padx=85, pady=1)
decode_button.place(x = 320, y = 450)


selected_method = tk.StringVar()
combo = ttk.Combobox(root,textvariable=selected_method, width=35)
combo['values'] = ["Baconova šifra", "Open-space metoda", "Metoda synonym", "Metoda synonym s baconovým šifrováním", "Huffmanovo kódování"]
combo['state'] = 'readonly'
combo.set('Choose steganographic method')
combo.place(x = 20, y = 300)
combo.bind('<<ComboboxSelected>>', month_changed)

root.mainloop()