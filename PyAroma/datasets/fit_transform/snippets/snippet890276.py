import re
import string
from fastai.text import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ...helpers.training import set_seed


def bow(self, X_train):
    self.n = X_train.shape[0]
    tokenizer = (tokenize_fixed if self.experiment.fixed_tokenizer else tokenize)
    if (self.experiment.vectorizer == 'tfidf'):
        self.vec = TfidfVectorizer(ngram_range=self.experiment.ngram_range, tokenizer=tokenizer, lowercase=self.experiment.lowercase, analyzer=self.experiment.analyzer, min_df=self.experiment.min_df, max_df=self.experiment.max_df, strip_accents='unicode', use_idf=1, smooth_idf=1, sublinear_tf=1)
    elif (self.experiment.vectorizer == 'count'):
        self.vec = CountVectorizer(ngram_range=self.experiment.ngram_range, tokenizer=tokenizer, analyzer=self.experiment.analyzer, lowercase=self.experiment.lowercase, min_df=self.experiment.min_df, max_df=self.experiment.max_df, strip_accents='unicode')
    else:
        raise Exception(f'Unknown vectorizer type: {self.experiment.vectorizer}')
    return self.vec.fit_transform(X_train)
