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


def get_clf(clf_method):
    mapping = {'MNB': (MultinomialNB, {'alpha': 0.1}), 'SGD': (SGDClassifier, {'loss': 'hinge', 'penalty': 'l2', 'alpha': 0.001, 'max_iter': 5, 'tol': None}), 'RandomForest': (RandomForestClassifier, {'max_depth': 5}), 'AdaBoost': (AdaBoostClassifier, {})}
    try:
        (method, parameters) = mapping[clf_method]
    except KeyError:
        error = 'Please make sure clf_method in "MNB", "SGD", "RandomForest" or "AdaBoost".'
        raise MethodNotFoundError(error)
    return method(**parameters)
