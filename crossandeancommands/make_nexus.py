"""
Create a nexus file from a Lexibank dataset.
"""
from lingpy import Wordlist
from lingpy.convert.strings import write_nexus
from lexibank_crossandean import Dataset as CA


def run(args):
    """Function runs the creation of a Nexus file."""
    dataset = CA()
    wordlist = Wordlist.from_cldf(
        str(dataset.cldf_dir.joinpath("cldf-metadata.json").as_posix()),
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

    blacklist_subgroups = {
            'Aymara',
            'Uru-Chipaya'
            }

    blacklist_borrowings = {
            'aymara',
            'esp',
            'uru'
            }

    D = {0: [c for c in wordlist.columns]}  # defines the header
    for idx in wordlist:
        if (
            wordlist[idx, "subgroup"] not in blacklist_subgroups and
            wordlist[idx, "doculect"] not in blacklist_languages and
            wordlist[idx, "borrowing"] not in blacklist_borrowings
        ):
            D[idx] = [wordlist[idx, c] for c in D[0]]

    wlnew = Wordlist(D)
    etd = wlnew.get_etymdict(ref="cogid")
    args.log.info(
        f"Created wordlist with {wlnew.width} languages, {len(etd)} "
        "concepts, and {wlnew.height} cognatesets"
        )

    write_nexus(
            wlnew,
            ref="cogid",
            mode="BEAST",
            filename=str(dataset.dir.joinpath('outputs', 'quechua_modern.nex'))
            )
    args.log.info("wrote data to file 'outputs/crossandean-beast.nex'")
    wlnew.output(
            "tsv",
            filename=str(dataset.dir.joinpath("outputs", "quechua_modern")),
            prettify=False,
            ignore="all")
    args.log.info("wrote wordlist data to file")
