"""
Create a nexus file from the most recent data on Edictor.
"""
from lingpy import Wordlist
from lingpy.convert.strings import write_nexus
from lexibank_crossandean import Dataset as CA


def run(args):

    ds = CA()
    wl = Wordlist.from_cldf(
        str(ds.cldf_dir.joinpath("cldf-metadata.json").as_posix()),
        # columns to be loaded from CLDF set
        columns=(
            "language_id",
            "concept_name",
            "segments",
            "language_subgroup",
            "borrowing",
            "cognacy"
            ),
        # a list of tuples of source and target
        namespace=(
            ("language_id", "doculect"),
            ("concept_name", "concept"),
            ("segments", "tokens"),
            ("language_subgroup", "subgroup"),
            ("cognacy", "cogid")
            )
        )

    # These are the blacklists for the nexus file
    blacklist_languages = {
            'CuzquenoAntiguo',
            'Anonimo',
            'SantoTomas',
            }

    blacklist_concepts = {
            'with',
            'small',
            'lip',
            'wing',
            'branch',
            'husband',
            'leg',
            'egg',
            'breast',
            'suck, to',
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
    etd = wlnew.get_etymdict(ref="cogid")
    args.log.info("Created wordlist with {0} languages, {1} concepts, and {2} cognatesets".format(
        wlnew.width, wlnew.height, len(etd)))

    # Word-parameterised nexus
    write_nexus(
            wlnew,
            ref="cogid",
            mode="BEASTWORDS",
            filename=str(ds.dir.joinpath('outputs', 'crossandean-beast_150.nex'))
            )
    args.log.info("wrote data to file 'outputs/crossandean-beast.nex'")
    wlnew.output(
            "tsv",
            filename=str(ds.dir.joinpath("outputs", "crossandean-cognates")),
            prettify=False,
            ignore="all")
    args.log.info("wrote wordlist data to file")
