import pickle
import sys
import numpy
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from . import Model


def __init__(self, **params):
    params['name'] = 'SVM'
    super(SVM, self).__init__(**params)
    self.model = LinearSVC(multi_class='crammer_singer')
