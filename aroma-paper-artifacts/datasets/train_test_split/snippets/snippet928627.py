import os
import pickle
import tarfile
import hashlib
import codecs
import urllib
import logging
import numpy as np
from collections import namedtuple
from urllib.request import urlretrieve
from .exceptions import *
from .common import *
from sklearn.feature_extraction._stop_words import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.datasets import load_files
from nltk.tokenize import word_tokenize
import jieba


def _train_test_split(cache, test_size=0.1):
    data_lst = list()
    target = list()
    filenames = list()
    data = cache['all']
    data_lst.extend(data.data)
    target.extend(data.target)
    filenames.extend(data.filenames)
    data.data = data_lst
    data.target = np.array(target)
    data.filenames = np.array(filenames)
    return train_test_split(data.data, data.target, test_size=test_size, random_state=0)
