import re
import string
from fastai.text import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ...helpers.training import set_seed


def predict_proba(self, X_test):
    test_term_doc = self.vec.transform(X_test)
    if (self.experiment.multinomial_type == 'manual'):
        preds = np.zeros((len(X_test), self.c))
        for i in range(0, self.c):
            (m, r) = self.models[i]
            preds[(:, i)] = m.predict_proba(test_term_doc.multiply(r))[(:, 1)]
    elif ((self.experiment.multinomial_type == 'multinomial') or (self.experiment.multinomial_type == 'ovr')):
        preds = self.models[0].predict_proba(test_term_doc)
    else:
        raise Exception(f'Unsupported multinomial_type {self.experiment.multinomial_type}')
    return preds
