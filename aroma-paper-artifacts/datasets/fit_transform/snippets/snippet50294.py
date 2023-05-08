from os.path import join, dirname, abspath
import sys
import copy
import torch
import random
import numpy as np
import pandas as pd
import evidence_inference.preprocess.preprocessor as preprocessor
import torch.nn as nn
from scipy import stats
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.feature_extraction.text import CountVectorizer


def bag_of_words(x_train, y_train, x_val, y_val, x_test, y_test, n=4):
    '\n    Transform data into b.o.w. w/ a max of 20k tokens.\n\n    @param x_train is the training data.\n    @param y_train is the training labels.\n    @param x_val   is the validation data.\n    @param y_val   is the validation labels.\n    @param x_test  is the training data.\n    @param y_test  is the test labels.\n    @param n       is the number of sections in the input data (text/ico/reasoning).\n    @return a bag of words representation of the data.\n    '
    (x_train, x_val, x_test) = (flatten(x_train), flatten(x_val), flatten(x_test))
    print('flatten')
    vectorizer = CountVectorizer(max_features=20000)
    X = vectorizer.fit_transform(x_train)
    print('trained')
    (y_train, y_val, y_test) = ((torch.tensor([[y] for y in x], dtype=torch.long).cuda() if USE_CUDA else torch.tensor([[y] for y in x], dtype=torch.long)) for x in (np.asarray(y_train), np.asarray(y_val), np.asarray(y_test)))
    print('y_s achieved.')
    return (fmt_n(X.toarray(), n), y_train, fmt_n(vectorizer.transform(x_val).toarray(), n), y_val, fmt_n(vectorizer.transform(x_test).toarray(), n), y_test)
