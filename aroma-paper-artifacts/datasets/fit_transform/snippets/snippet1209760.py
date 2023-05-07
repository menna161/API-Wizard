from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import itertools
from copy import copy
import pickle, sys, re, json


def generate_vocab(qa_pairs, instance_id):
    questions = [qa_pair['question'] for qa_pair in qa_pairs]
    answers = [qa_pair['answer'] for qa_pair in qa_pairs]
    questions_cleaned = list(map(clean_str, list(questions)))
    answers_cleaned = list(map(clean_str, answers))
    count_vect_q = CountVectorizer(stop_words='english')
    counts_q = count_vect_q.fit_transform(questions_cleaned)
    count_vect_a = CountVectorizer(stop_words='english')
    counts_a = count_vect_a.fit_transform(answers_cleaned)
    q_vocab = (set(count_vect_q.get_feature_names()) & terms_dict[instance_id]['context_terms'])
    a_vocab = (set(count_vect_a.get_feature_names()) & terms_dict[instance_id]['resp_terms'])
    q_vocab_dict = {}
    a_vocab_dict = {}
    for term in q_vocab:
        q_vocab_dict[term] = 1
    for term in a_vocab:
        a_vocab_dict[term] = 1
    return (q_vocab_dict, a_vocab_dict)
