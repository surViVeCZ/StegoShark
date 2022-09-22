
![CI](https://github.com/surViVeCZ/StegoShark/actions/workflows/CI.yml/badge.svg)
![github repo size](https://img.shields.io/github/repo-size/surViVeCZ/StegoShark)
![Python versions](https://img.shields.io/pypi/pyversions/Django)

[![IMG-20220922-112510-modified.png](https://i.postimg.cc/vTC5yqHB/IMG-20220922-112510-modified.png)](https://postimg.cc/H84r4tMD)

__Autor:__ Petr Pouč

__Datum:__ 25. 4. 2022

Tento projekt je součástí bakalářské práce ["Digitální textová steganografie"](https://www.fit.vut.cz/study/thesis/24328/).

***

# Instalace

```
chmod +x install.sh
./install.sh
```

# Vstupní argumenty
```
-i <inputfile> [-e/-d] -s <secret_message> [-b/-w/-r/--own1/--own2]
```
__-i__ = vstupní soubor formátu .docx/.txt

__-e__ = encode (přejeme si vložit tajnou zprávu do zvoleného souboru)

__-d__ = decode (přejeme si dešifrovat zvolený soubor)

__-s__ = zvolená tajná zpráva, kterou si přejeme ukrýt 

__-b__ = šifrování/dešifrování Baconovou šifrou

__-w__ = šifrování/dešifrování Open-space metodou

__-r__ = šifrování/dešifrování metodou synonym

__--own1__ = šifrování/dešifrování metodou synonym využívající Baconova šifrování

__--own2__ = šifrování/dešifrování metodou synonym využívající Huffmanova kódování

## Příklady spuštění
Šifrování Baconovou šifrou
```
python3 steganography.py -i cover_files/bacon/adele.docx -e -s "tajnazprava." -b 
```
Dešifrování Baconovou šifrou
```
python3 steganography.py -i encoded/bacon_adele.docx -d -s -b 
```
Spuštění automatizovaných testů
```
python3 tests.py
```
Spuštění aplikace
```
pomocí tlačítka run code
například ve Visual studio code pomocí - ctrl + alt + N
```
