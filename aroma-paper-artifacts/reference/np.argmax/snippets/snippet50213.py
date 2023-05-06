from os.path import join, dirname, abspath
import sys
import re
import string
import numpy as np
from functools import reduce
from pattern.en import lexeme
from nltk.corpus import wordnet
from evidence_inference.experiments.model_0_paper_experiment import get_data
import evidence_inference.preprocess.preprocessor as preprocessor
from evidence_inference.models.heuristic_utils import parse_p_value, sig_or_ns_pval, split_sentences, strip_punctuation
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import pdb


def locate_probable_sentence(text, out, inter, cmp):
    sentences = split_sentences(text)
    sentences = list(filter((lambda x: (x != '')), sentences))
    dict_of_words = list(map(generate_word_dict, sentences))
    point_arr = ([None] * len(sentences))
    idx = 0
    for d in dict_of_words:
        points = 0
        points += reduce((lambda y, x: ((y + 1) if (x in d) else y)), out.split(' '), 0)
        points += reduce((lambda y, x: ((y + 1) if (x in d) else y)), inter.split(' '), 0)
        points += reduce((lambda y, x: ((y + 1) if (x in d) else y)), inter.split(' '), 0)
        point_arr[idx] = points
        idx += 1
    loc_best = np.argmax(point_arr)
    likely_sentence = sentences[loc_best]
    return (likely_sentence, point_arr)
