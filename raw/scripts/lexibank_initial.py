import attr
from pathlib import Path

from pylexibank import Concept, Language, Lexeme
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar

from clldutils.misc import slug


#@attr.s
#class CustomConcept(Concept):
#    Chinese_Gloss = attr.ib(default=None)
#    Number = attr.ib(default=None)

@attr.s
class CustomLexeme(Lexeme):
    ID = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    ID = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "crossandean"
    language_class = CustomLanguage
    lexeme_class = CustomLexeme

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        concepts = {}
        for concept in self.concepts:
            idx = concept['NUMBER']+'_'+slug(concept['ENGLISH'])
            args.writer.add_concept(
                    ID=idx,
                    Name=concept['ENGLISH'],
                    Concepticon_ID=concept['CONCEPTICON_ID'],
                    Concepticon_Gloss=concept['CONCEPTICON_GLOSS']
                    )
            concepts[concept['ENGLISH']] = idx
        languages = args.writer.add_languages(lookup_factory='ID')
        for idx, language, concept, form, comments, source in progressbar(self.raw_dir.read_csv(
                'crossandean.csv', delimiter=',')[1:]):
            args.writer.add_forms_from_value(
                    Language_ID=languages[language],
                    Parameter_ID=concepts[concept],
                    Value=form,
                    Source=source,
                    Comment=comments
                    )
            
