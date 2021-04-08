from lexibank_crossandean import Dataset
from lingpy import *
from lingpy.compare.partial import *
from lexibase.lexibase import LexiBase


cols = ['concept_id', 'concept_name', 'language_id', 'language_name', 'value',
        'form', 'segments', 'glottocode', 'concept_concepticon_id',
        'comment']


DS = Dataset()
languages = {l["ID"]: l["SubGroup"] for l in DS.languages}
concepts = {c["ENGLISH"]: c["SPANISH"] for c in DS.concepts}
lex = Partial.from_cldf(DS.cldf_dir.joinpath('cldf-metadata.json'),
        columns=cols)
lex.partial_cluster(method='sca', threshold=0.45, ref="cogids")
alms = Alignments(lex, ref="cogids")
alms.align()
alms.add_entries("morphemes", "tokens", lambda x: "")
alms.add_entries("subgroup", "doculect", lambda x: languages[x])
alms.add_entries("spanish", "concept", lambda x: concepts[x])
alms.add_entries("note", "comment", lambda x: x if x else "")


D = {0: ["doculect", "subgroup", "concept", "spanish", "value", "form",
    "tokens", "cogids", "morphemes", "alignment", "note"]}
for idx in alms:
    D[idx] = [alms[idx, h] for h in D[0]]
lex = LexiBase(D, dbase="crossandean.sqlite3")
lex.create("crossandean")
