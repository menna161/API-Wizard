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


def return_model(mode, **kwargs):
    if inspect.isclass(mode):
        assert (getattr(mode, 'fit', None) is not None), 'Custom model family should have a fit() method'
        model = mode(**kwargs)
    elif (mode == 'logistic'):
        solver = kwargs.get('solver', 'liblinear')
        n_jobs = kwargs.get('n_jobs', None)
        max_iter = kwargs.get('max_iter', 5000)
        model = LogisticRegression(solver=solver, n_jobs=n_jobs, max_iter=max_iter, random_state=666)
    elif (mode == 'Tree'):
        model = DecisionTreeClassifier(random_state=666)
    elif (mode == 'RandomForest'):
        n_estimators = kwargs.get('n_estimators', 50)
        model = RandomForestClassifier(n_estimators=n_estimators, random_state=666)
    elif (mode == 'GB'):
        n_estimators = kwargs.get('n_estimators', 50)
        model = GradientBoostingClassifier(n_estimators=n_estimators, random_state=666)
    elif (mode == 'AdaBoost'):
        n_estimators = kwargs.get('n_estimators', 50)
        model = AdaBoostClassifier(n_estimators=n_estimators, random_state=666)
    elif (mode == 'SVC'):
        kernel = kwargs.get('kernel', 'rbf')
        model = SVC(kernel=kernel, random_state=666)
    elif (mode == 'LinearSVC'):
        model = LinearSVC(loss='hinge', random_state=666)
    elif (mode == 'GP'):
        model = GaussianProcessClassifier(random_state=666)
    elif (mode == 'KNN'):
        n_neighbors = kwargs.get('n_neighbors', 5)
        model = KNeighborsClassifier(n_neighbors=n_neighbors)
    elif (mode == 'NB'):
        model = MultinomialNB()
    elif (mode == 'linear'):
        model = LinearRegression(random_state=666)
    elif (mode == 'ridge'):
        alpha = kwargs.get('alpha', 1.0)
        model = Ridge(alpha=alpha, random_state=666)
    elif ('conv' in mode):
        tf.reset_default_graph()
        address = kwargs.get('address', 'weights/conv')
        hidden_units = kwargs.get('hidden_layer_sizes', [20])
        activation = kwargs.get('activation', 'relu')
        weight_decay = kwargs.get('weight_decay', 0.0001)
        learning_rate = kwargs.get('learning_rate', 0.001)
        max_iter = kwargs.get('max_iter', 1000)
        early_stopping = kwargs.get('early_stopping', 10)
        warm_start = kwargs.get('warm_start', False)
        batch_size = kwargs.get('batch_size', 256)
        kernel_sizes = kwargs.get('kernel_sizes', [5])
        strides = kwargs.get('strides', [5])
        channels = kwargs.get('channels', [1])
        validation_fraction = kwargs.get('validation_fraction', 0.0)
        global_averaging = kwargs.get('global_averaging', 0.0)
        optimizer = kwargs.get('optimizer', 'sgd')
        if (mode == 'conv'):
            model = CShapNN(mode='classification', batch_size=batch_size, max_epochs=max_iter, learning_rate=learning_rate, weight_decay=weight_decay, validation_fraction=validation_fraction, early_stopping=early_stopping, optimizer=optimizer, warm_start=warm_start, address=address, hidden_units=hidden_units, strides=strides, global_averaging=global_averaging, kernel_sizes=kernel_sizes, channels=channels, random_seed=666)
        elif (mode == 'conv_reg'):
            model = CShapNN(mode='regression', batch_size=batch_size, max_epochs=max_iter, learning_rate=learning_rate, weight_decay=weight_decay, validation_fraction=validation_fraction, early_stopping=early_stopping, optimizer=optimizer, warm_start=warm_start, address=address, hidden_units=hidden_units, strides=strides, global_averaging=global_averaging, kernel_sizes=kernel_sizes, channels=channels, random_seed=666)
    elif ('NN' in mode):
        solver = kwargs.get('solver', 'adam')
        hidden_layer_sizes = kwargs.get('hidden_layer_sizes', (20,))
        if isinstance(hidden_layer_sizes, list):
            hidden_layer_sizes = list(hidden_layer_sizes)
        activation = kwargs.get('activation', 'relu')
        learning_rate_init = kwargs.get('learning_rate', 0.001)
        max_iter = kwargs.get('max_iter', 5000)
        early_stopping = kwargs.get('early_stopping', False)
        warm_start = kwargs.get('warm_start', False)
        if (mode == 'NN'):
            model = MLPClassifier(solver=solver, hidden_layer_sizes=hidden_layer_sizes, activation=activation, learning_rate_init=learning_rate_init, warm_start=warm_start, max_iter=max_iter, early_stopping=early_stopping)
        if (mode == 'NN_reg'):
            model = MLPRegressor(solver=solver, hidden_layer_sizes=hidden_layer_sizes, activation=activation, learning_rate_init=learning_rate_init, warm_start=warm_start, max_iter=max_iter, early_stopping=early_stopping)
    else:
        raise ValueError('Invalid mode!')
    return model
