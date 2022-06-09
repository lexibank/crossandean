from pyedictor import fetch
from lingpy import *
from tabulate import tabulate

errors = []
count = 1
wl = fetch('crossandean', to_lingpy=True, base_url="https://lingulist.de/edictor/")
for idx, doculect, concept, tokens, alm, cogids in wl.iter_rows("doculect", "concept", "tokens", "alignment", "cogids"):
    if len(tokens.n) != len(cogids) or len(basictypes.lists(alm).n) != len(tokens.n):
        errors += [[count, idx, doculect, concept, str(tokens), " ".join(alm), str(basictypes.ints(cogids))]]
        count += 1
print(tabulate(errors))