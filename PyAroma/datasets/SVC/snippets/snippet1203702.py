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


def marginals(clf, X, y, X_test, y_test, c=None, tol=0.0, trials=3000, mean_score=None, metric='accuracy'):
    if (metric == 'auc'):

        def score_func(clf, a, b):
            return roc_auc_score(b, clf.predict_proba(a)[(:, 1)])
    elif (metric == 'accuracy'):

        def score_func(clf, a, b):
            return clf.score(a, b)
    else:
        raise ValueError('Wrong metric!')
    if (mean_score is None):
        accs = []
        for _ in range(100):
            bag_idxs = np.random.choice(len(y_test), len(y_test))
            accs.append(score_func(clf, X_test[bag_idxs], y_test[bag_idxs]))
        mean_score = np.mean(accs)
    (marginals, idxs) = ([], [])
    for trial in range(trials):
        if ((((10 * (trial + 1)) / trials) % 1) == 0):
            print('{} out of {}'.format((trial + 1), trials))
        (marginal, idx) = one_iteration(clf, X, y, X_test, y_test, mean_score, tol=tol, c=c, metric=metric)
        marginals.append(marginal)
        idxs.append(idx)
    return (np.array(marginals), np.array(idxs))
