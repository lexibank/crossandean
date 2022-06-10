"""
Create a nexus file from the most recent data on Edictor.
"""
from pyedictor import fetch
from lingpy import Wordlist
from lingpy.convert.strings import write_nexus

def run(args):

    with open("./outputs/crossandean.tsv", "w",
            encoding="utf-8") as f:
            f.write(fetch("crossandean",
                    columns=[
                            "ID", 
                            "ALIGNMENT", 
                            "COGIDS", 
                            "CONCEPT", 
                            "DOCULECT", 
                            "FORM", 
                            "TOKENS", 
                            "BORROWING", 
                            "SOURCE", 
                            "SUBGROUP"
                            ]
                    ))

    wl = Wordlist('./outputs/crossandean.tsv')                        
    

    # These are the blacklists for the nexus file
    blacklist_concepts = [
            'star', 
            'green', 
            'with', 
            'small', 
            'lip', 
            'wing', 
            'breast', 
            'suck, to', 
            'husband', 
            'branch'
            ]

    blacklist_subgroups = [
            'Aymara', 
            'Uru-Chipaya'
            ]

    blacklist_borrowings = [
            'aymara', 
            'esp', 
            'uru'
            ]

    blacklist_historical = [
            'CuzquenoAntiguo',
            'Anonimo', 
            'SantoTomas',
            ]

    # This output creates a second wordlist with only the filtered data. 
    wl.output(
            'tsv',
            filename = './outputs/filtered',
            subset = True,
            rows = dict(
                    doculect = 'not in' + str(blacklist_historical),
                    borrowing = 'not in' + str(blacklist_borrowings),
                    subgroup = 'not in' + str(blacklist_subgroups),
                    concept = 'not in' + str(blacklist_concepts)
                    )
            )

    wl_filtered = Wordlist('./outputs/filtered.tsv')

    # Word-parameterised nexus
    write_nexus(
            wl_filtered,
            ref="cogids", 
            mode="BEASTWORDS",
            filename='./outputs/crossandean_beast.nex'
            )