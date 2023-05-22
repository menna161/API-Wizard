import os
import json
import fire
import numpy as np
from scipy import sparse
from sklearn.model_selection import PredefinedSplit, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer


def main(data_dir, log_dir, source='xl-1542M-k40', n_train=500000, n_valid=10000, n_jobs=None, verbose=False):
    (train_texts, train_labels) = load_split(data_dir, source, 'train', n=n_train)
    (valid_texts, valid_labels) = load_split(data_dir, source, 'valid', n=n_valid)
    (test_texts, test_labels) = load_split(data_dir, source, 'test')
    vect = TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_features=(2 ** 21))
    train_features = vect.fit_transform(train_texts)
    valid_features = vect.transform(valid_texts)
    test_features = vect.transform(test_texts)
    model = LogisticRegression(solver='liblinear')
    params = {'C': [(1 / 64), (1 / 32), (1 / 16), (1 / 8), (1 / 4), (1 / 2), 1, 2, 4, 8, 16, 32, 64]}
    split = PredefinedSplit((([(- 1)] * n_train) + ([0] * n_valid)))
    search = GridSearchCV(model, params, cv=split, n_jobs=n_jobs, verbose=verbose, refit=False)
    search.fit(sparse.vstack([train_features, valid_features]), (train_labels + valid_labels))
    model = model.set_params(**search.best_params_)
    model.fit(train_features, train_labels)
    valid_accuracy = (model.score(valid_features, valid_labels) * 100.0)
    test_accuracy = (model.score(test_features, test_labels) * 100.0)
    data = {'source': source, 'n_train': n_train, 'valid_accuracy': valid_accuracy, 'test_accuracy': test_accuracy}
    print(data)
    json.dump(data, open(os.path.join(log_dir, f'{source}.json'), 'w'))
