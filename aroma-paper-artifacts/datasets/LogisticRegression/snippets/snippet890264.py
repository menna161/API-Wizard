import re
import string
from fastai.text import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ...helpers.training import set_seed


def get_class_column(y, classIdx):
    if (len(y.shape) == 1):
        return (y == classIdx)
    else:
        return y.iloc[(:, classIdx)]
