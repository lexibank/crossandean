from pyedictor import fetch
from lingpy import Alignments, Wordlist, LexStat


with open("crossandean.tsv", "w",
        encoding="utf-8") as f:
        f.write(fetch("crossandean",
                columns=["ID", "ALIGNMENT", "COGIDS", "CONCEPT",
                "DOCULECT", "FORM", 
                "SPANISH", "TOKENS", "VALUE", "BORROWING", "NOTE",
                "SOURCE", "SUBGROUP"]
                ))

#wl = Wordlist("crossandean.tsv")
#lex = LexStat(wl, segments='tokens', check=True)

# tried with all of wl/lex/tsv-file
alm = Alignments("crossandean.tsv", ref = 'COGIDS', transcription = "FORM") 

#alm.align()
