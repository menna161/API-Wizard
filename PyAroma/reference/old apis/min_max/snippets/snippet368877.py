from __future__ import absolute_import, division, unicode_literals
import logging
import os
import pickle
import re
import time
from builtins import object
from collections import defaultdict
from importlib import import_module
import numpy as np
import pandas as pd
from sklearn import decomposition
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, ExpSineSquared, Matern, RationalQuadratic
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from atm.constants import Metrics
from atm.encoder import DataEncoder
from atm.method import Method
from atm.metrics import cross_validate_pipeline, test_pipeline


def _make_pipeline(self):
    '\n        Makes the classifier as well as scaling or dimension reduction steps.\n        '
    steps = []
    hyperparameters = {k: v for (k, v) in list(self.params.items()) if (k not in Model.ATM_KEYS)}
    atm_params = {k: v for (k, v) in list(self.params.items()) if (k in Model.ATM_KEYS)}
    hyperparameters = self._special_conversions(hyperparameters)
    classifier = self.class_(**hyperparameters)
    if ((Model.PCA in atm_params) and atm_params[Model.PCA]):
        whiten = ((Model.WHITEN in atm_params) and atm_params[Model.WHITEN])
        pca_dims = atm_params[Model.PCA_DIMS]
        if (pca_dims < 1):
            dimensions = int((pca_dims * float(self.num_features)))
            logger.info(('Using PCA to reduce %d features to %d dimensions' % (self.num_features, dimensions)))
            pca = decomposition.PCA(n_components=dimensions, whiten=whiten)
            steps.append(('pca', pca))
    if atm_params.get(Model.SCALE):
        steps.append(('standard_scale', StandardScaler()))
    elif self.params.get(Model.MINMAX):
        steps.append(('minmax_scale', MinMaxScaler()))
    steps.append((self.method, classifier))
    self.pipeline = Pipeline(steps)
