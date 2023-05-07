import re
import string
from fastai.text import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ...helpers.training import set_seed


def validate(self, X_test, y_test):
    acc = (np.argmax(self.predict_proba(X_test), axis=1) == y_test).mean()
    return acc
