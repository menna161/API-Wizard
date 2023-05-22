import re
import string
from fastai.text import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ...helpers.training import set_seed


def train_models(self, y_train):
    self.models = []
    if (self.experiment.multinomial_type == 'manual'):
        for i in range(0, self.c):
            (m, r) = self.get_mdl(get_class_column(y_train, i))
            self.models.append((m, r))
    elif ((self.experiment.multinomial_type == 'multinomial') or (self.experiment.multinomial_type == 'ovr')):
        m = LogisticRegression(C=self.experiment.C, penalty=self.experiment.penalty, dual=self.experiment.dual, solver=self.experiment.solver, max_iter=self.experiment.max_iter, multi_class=self.experiment.multinomial_type, class_weight=self.experiment.class_weight)
        x_nb = self.trn_term_doc
        self.models.append(m.fit(x_nb, y_train))
    else:
        raise Exception(f'Unsupported multinomial_type {self.experiment.multinomial_type}')
