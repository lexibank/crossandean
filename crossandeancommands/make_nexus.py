"""
Create a nexus file from the most recent data on Edictor.
"""
from lingpy import Wordlist
from lingpy.convert.strings import write_nexus
from lexibank_crossandean import Dataset as CA
from pathlib import Path


def run(args):

    ds = CA()
    wl = Wordlist.from_cldf(
        str(ds.cldf_dir.joinpath("cldf-metadata.json").as_posix()),
        # columns to be loaded from CLDF set
        columns=(
            "language_id",
            "parameter_id",
            "segments",
            "language_subgroup",
            "borrowing",
            "cogid_cognateset_id"
            ),
        # a list of tuples of source and target
        namespace=(
            ("language_id", "doculect"),
            ("parameter_id", "concept"),
            ("segments", "tokens"),
            ("language_subgroup", "subgroup"),
            ("cogid_cognateset_id", "cogids")
            )
        )

    # These are the blacklists for the nexus file
    blacklist_languages = {
            'CuzquenoAntiguo',
            'Anonimo',
            'SantoTomas',
            }

    blacklist_concepts = {
            'star',
            'green',
            'with',
            'small',
            'lip',
            'wing',
            'breast',
            'suck,to',
            'husband',
            'branch'
            }

    blacklist_subgroups = {
            'Aymara',
            'Uru-Chipaya'
            }

    blacklist_borrowings = {
            'aymara',
            'esp',
            'uru'
            }

    D = {0: [c for c in wl.columns]}  # defines the header
    for idx in wl:
        if (
            wl[idx, "subgroup"] not in blacklist_subgroups and
            wl[idx, "doculect"] not in blacklist_languages and
            wl[idx, "concept"] not in blacklist_concepts and
            wl[idx, "borrowing"] not in blacklist_borrowings
        ):
            D[idx] = [wl[idx, c] for c in D[0]]

    wlnew = Wordlist(D)

    # Word-parameterised nexus
    write_nexus(
            wlnew,
            ref="cogids",
            mode="BEASTWORDS",
            filename='./outputs/crossandean_beast.nex'
            )
