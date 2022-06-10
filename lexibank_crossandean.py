from pathlib import Path

import attr
import pylexibank
from clldutils.misc import slug
from lingpy import Wordlist
from pyedictor import fetch


@attr.s
class CustomLexeme(pylexibank.Lexeme):
    Borrowing = attr.ib(default=None)


@attr.s
class CustomLanguage(pylexibank.Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    SubGroup = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "crossandean"
    language_class = CustomLanguage
    lexeme_class = CustomLexeme

    form_spec = pylexibank.FormSpec(separators=",")

    def cmd_download(self, args):
        print("updating ...")
        with open(self.raw_dir.joinpath("crossandean.tsv"), "w", encoding="utf-8") as f:
            f.write(
                fetch(
                    "crossandean",
                    columns=[
                        "ALIGNMENT",
                        "COGIDS",
                        "CONCEPT",
                        "DOCULECT",
                        "SUBGROUP",
                        "FORM",
                        "SPANISH",
                        "TOKENS",
                        "VALUE",
                        "BORROWING",
                        "NOTE",
                        "SOURCE",
                    ],
                )
            )

    def cmd_makecldf(self, args):
        args.writer.add_sources()

        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split("-")[-1] + "_" + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )

            concepts[concept.english] = idx

        languages = args.writer.add_languages(lookup_factory="ID")

        errors = set()
        wl = Wordlist(str(self.raw_dir.joinpath("crossandean.tsv")))

        for (
            idx,
            language,
            concept,
            value,
            form,
            tokens,
            comment,
            source,
            borrowing,
            cogids,
        ) in pylexibank.progressbar(
            wl.iter_rows(
                "doculect",
                "concept",
                "value",
                "form",
                "tokens",
                "note",
                "source",
                "borrowing",
                "cogids",
            ),
            desc="cldfify",
        ):
            if language not in languages:
                errors.add(("language", language))
            elif concept not in concepts:
                errors.add(("concept", concept))
            elif tokens:
                lexeme = args.writer.add_form_with_segments(
                    Parameter_ID=concepts[concept],
                    Language_ID=language,
                    Value=value.strip() or form.strip(),
                    Form=form.strip(),
                    Segments=tokens,
                    Source=source,
                    Borrowing=borrowing,
                    Comment=comment,
                )

                this_cogid = "".join([str(x) for x in cogids if x])
                args.writer.add_cognate(lexeme=lexeme, Cognateset_ID=this_cogid, Source=source)

        for typ, error in sorted(errors):
            print(typ + ": " + error)
