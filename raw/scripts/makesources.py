from csvw.dsv import UnicodeDictReader
from collections import defaultdict
from pyedictor import fetch
from lexibase import LexiBase

data = {}
source2lang = defaultdict(set)
out = []
sla = {}
with UnicodeDictReader("crossandean_original_raw.csv", delimiter=",") as reader:
    for i, row in enumerate(reader):
        data[i+1] = row
        source2lang[row["LANGUAGE"]].add(row["SOURCE"])
        out += [[row["LANGUAGE"], row["FORM"], row["SOURCE"]]]
        sla[row["LANGUAGE"], row["FORM"]] = row["SOURCE"]
with open("sourcelookup.tsv", "w") as f:
    f.write("DOCULECT\tFORM\tSOURCE\n")
    for row in out:
        f.write("\t".join(row)+"\n")

for k, vals in source2lang.items():
    if len(vals) > 1:
        print(k, vals)


wl = fetch("crossandean", to_lingpy=True,
    columns=["ALIGNMENT", "COGIDS", "CONCEPT",
                        "DOCULECT", "FORM", 
                        "SPANISH", "TOKENS", "VALUE", "BORROWING", "NOTE",
                        "SOURCE", "SUBGROUP"]
        )
count = 0
for idx, language, form in wl.iter_rows("doculect", "value"):
    if (language, form) in sla:
        wl[idx, "source"] = sla[language, form]
    else:
        count += 1

print(count)

lex = LexiBase(wl)
lex.db = "crossandean-new.sqlite3"
lex.create("crossandean")

lex.output('tsv', filename="dummy", ignore="all")
