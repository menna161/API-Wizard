import re
import string
from fastai.text import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ...helpers.training import set_seed


def get_mdl(self, y):
    y = y.values
    r = np.log((self.pr(1, y) / self.pr(0, y)))
    m = LogisticRegression(C=self.experiment.C, penalty=self.experiment.penalty, dual=self.experiment.dual, solver=self.experiment.solver, max_iter=self.experiment.max_iter, class_weight=self.experiment.class_weight)
    x_nb = self.trn_term_doc.multiply(r)
    return (m.fit(x_nb, y), r)
