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


def label_generator(problem, X, param, difficulty=1, beta=None, important=None):
    if ((important is None) or (important > X.shape[(- 1)])):
        important = X.shape[(- 1)]
    dim_latent = sum([(important ** i) for i in range(1, (difficulty + 1))])
    if (beta is None):
        beta = np.random.normal(size=[1, dim_latent])
    important_dims = np.random.choice(X.shape[(- 1)], important, replace=False)
    funct_init = (lambda inp: np.sum((beta * generate_features(inp[(:, important_dims)], difficulty)), (- 1)))
    batch_size = max(100, min(len(X), (10000000 // dim_latent)))
    y_true = np.zeros(len(X))
    while True:
        try:
            for itr in range(int(np.ceil((len(X) / batch_size)))):
                y_true[(itr * batch_size):((itr + 1) * batch_size)] = funct_init(X[(itr * batch_size):((itr + 1) * batch_size)])
            break
        except MemoryError:
            batch_size = (batch_size // 2)
    (mean, std) = (np.mean(y_true), np.std(y_true))
    funct = (lambda x: ((np.sum((beta * generate_features(x[(:, important_dims)], difficulty)), (- 1)) - mean) / std))
    y_true = ((y_true - mean) / std)
    if (problem is 'classification'):
        y_true = logistic.cdf((param * y_true))
        y = (np.random.random(X.shape[0]) < y_true).astype(int)
    elif (problem is 'regression'):
        y = (y_true + (param * np.random.normal(size=len(y_true))))
    else:
        raise ValueError('Invalid problem specified!')
    return (beta, y, y_true, funct)
