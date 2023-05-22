import re
import itertools
import pandas as pd
from flashtext import KeywordProcessor
from processing.preprocessing import create_spacy_clean, create_stem, remove_continuous_duplicates
from helper_data.entity_dictionary import create_entity_dictionary


def process_data(val1, val2):
    derived_train = pd.DataFrame()
    kp = create_synonym_dictonary(val2)
    print('> Data Augmentation')
    for val in val1.values.tolist():
        derived_train = pd.concat([derived_train, create_derived(kp, val, val2)], sort=True)
    val3 = pd.concat([val1, derived_train])
    val3.drop_duplicates(inplace=True)
    print('> Preprocessing')
    val3.text = val3.text.apply(create_spacy_clean)
    val3.text = val3.text.apply(remove_continuous_duplicates)
    val3.drop_duplicates(inplace=True)
    val3 = val3.sample(frac=1).reset_index(drop=True)
    print('> Entity Dictionary')
    entity_extractor = create_entity_dictionary(val2)
    val3['text'] = val3['text'].apply(add_sos_eos)
    return (val3, entity_extractor)
