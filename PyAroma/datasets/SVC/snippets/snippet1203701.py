import os
import sys
import numpy as np
import inspect
from scipy.stats import logistic
from scipy.stats import spearmanr
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.base import clone
import inspect
from Shapley import ShapNN, CShapNN
from multiprocessing import dummy as multiprocessing
from sklearn.metrics import roc_auc_score, f1_score
import warnings
import tensorflow as tf
import matplotlib.pyplot as plt


def one_iteration(clf, X, y, X_test, y_test, mean_score, tol=0.0, c=None, metric='accuracy'):
    'Runs one iteration of TMC-Shapley.'
    if (metric == 'auc'):

        def score_func(clf, a, b):
            return roc_auc_score(b, clf.predict_proba(a)[(:, 1)])
    elif (metric == 'accuracy'):

        def score_func(clf, a, b):
            return clf.score(a, b)
    else:
        raise ValueError('Wrong metric!')
    if (c is None):
        c = {i: np.array([i]) for i in range(len(X))}
    (idxs, marginal_contribs) = (np.random.permutation(len(c.keys())), np.zeros(len(X)))
    new_score = (((np.max(np.bincount(y)) * 1.0) / len(y)) if (np.mean(((y // 1) == (y / 1))) == 1) else 0.0)
    start = 0
    if start:
        (X_batch, y_batch) = (np.concatenate([X[c[idx]] for idx in idxs[:start]]), np.concatenate([y[c[idx]] for idx in idxs[:start]]))
    else:
        (X_batch, y_batch) = (np.zeros(((0,) + tuple(X.shape[1:]))), np.zeros(0).astype(int))
    for (n, idx) in enumerate(idxs[start:]):
        try:
            clf = clone(clf)
        except:
            clf.fit(np.zeros(((0,) + X.shape[1:])), y)
        old_score = new_score
        (X_batch, y_batch) = (np.concatenate([X_batch, X[c[idx]]]), np.concatenate([y_batch, y[c[idx]]]))
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            try:
                clf.fit(X_batch, y_batch)
                temp_score = score_func(clf, X_test, y_test)
                if ((temp_score > (- 1)) and (temp_score < 1.0)):
                    new_score = temp_score
            except:
                continue
        marginal_contribs[c[idx]] = ((new_score - old_score) / len(c[idx]))
        if ((np.abs((new_score - mean_score)) / mean_score) < tol):
            break
    return (marginal_contribs, idxs)
