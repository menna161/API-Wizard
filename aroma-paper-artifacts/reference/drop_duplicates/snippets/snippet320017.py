import re
import itertools
import pandas as pd
from flashtext import KeywordProcessor
from processing.preprocessing import create_spacy_clean, create_stem, remove_continuous_duplicates
from helper_data.entity_dictionary import create_entity_dictionary


def no_entity_process_data(val1):
    print('> Preprocessing')
    val1.text = val1.text.apply(create_spacy_clean)
    val1.drop_duplicates(inplace=True)
    val1 = val1.sample(frac=1).reset_index(drop=True)
    entity_extractor = KeywordProcessor()
    val1['text'] = val1['text'].apply(add_sos_eos)
    return (val1, entity_extractor)
