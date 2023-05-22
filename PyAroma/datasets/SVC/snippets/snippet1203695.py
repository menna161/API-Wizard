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


def convergence_plots(marginals):
    plt.rcParams['figure.figsize'] = (15, 15)
    for (i, idx) in enumerate(np.arange(min(25, marginals.shape[(- 1)]))):
        plt.subplot(5, 5, (i + 1))
        plt.plot((np.cumsum(marginals[(:, idx)]) / np.arange(1, (len(marginals) + 1))))
