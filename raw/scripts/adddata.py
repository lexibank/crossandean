from segments import Tokenizer
from lexibase.lexibase import LexiBase
from csvw.dsv import UnicodeDictReader
from lingpy import *
prof = Tokenizer('addons-2021-05/Azuay.tsv')
with UnicodeDictReader("addons-2021-05/Azuay.csv") as reader:
    data = [row for row in reader]

lex = LexiBase.from_dbase(
        table="crossandean",
        dbase="crossandean.sqlite3",
        )

D = {0: ["concept", "spanish", "form", "note", "doculect",]}
for i, row in enumerate(data):
    D[i+1] = [row[h] for h in D[0]]

wl = Wordlist(D)
wl.add_entries('tokens', "form", lambda x: prof(x, column="IPA").split())

lex.add_data(wl)


