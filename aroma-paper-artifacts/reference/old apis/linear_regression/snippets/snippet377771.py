import dill
import os
import sys
from quantile_ml import utils_categorical_ensembling
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesRegressor, AdaBoostRegressor, GradientBoostingRegressor, GradientBoostingClassifier, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.linear_model import RandomizedLasso, RandomizedLogisticRegression, RANSACRegressor, LinearRegression, Ridge, Lasso, ElasticNet, LassoLars, OrthogonalMatchingPursuit, BayesianRidge, ARDRegression, SGDRegressor, PassiveAggressiveRegressor, LogisticRegression, RidgeClassifier, SGDClassifier, Perceptron, PassiveAggressiveClassifier
from sklearn.cluster import MiniBatchKMeans
from quantile_ml import utils
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMRegressor, LGBMClassifier
from tensorflow import logging
from keras.constraints import maxnorm
from keras.layers import Dense, Dropout
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.models import Sequential
from keras.models import load_model as keras_load_model
from keras import regularizers
from keras.wrappers.scikit_learn import KerasRegressor, KerasClassifier


def get_name_from_model(model):
    if isinstance(model, LogisticRegression):
        return 'LogisticRegression'
    if isinstance(model, RandomForestClassifier):
        return 'RandomForestClassifier'
    if isinstance(model, RidgeClassifier):
        return 'RidgeClassifier'
    if isinstance(model, GradientBoostingClassifier):
        return 'GradientBoostingClassifier'
    if isinstance(model, ExtraTreesClassifier):
        return 'ExtraTreesClassifier'
    if isinstance(model, AdaBoostClassifier):
        return 'AdaBoostClassifier'
    if isinstance(model, SGDClassifier):
        return 'SGDClassifier'
    if isinstance(model, Perceptron):
        return 'Perceptron'
    if isinstance(model, PassiveAggressiveClassifier):
        return 'PassiveAggressiveClassifier'
    if isinstance(model, LinearRegression):
        return 'LinearRegression'
    if isinstance(model, RandomForestRegressor):
        return 'RandomForestRegressor'
    if isinstance(model, Ridge):
        return 'Ridge'
    if isinstance(model, ExtraTreesRegressor):
        return 'ExtraTreesRegressor'
    if isinstance(model, AdaBoostRegressor):
        return 'AdaBoostRegressor'
    if isinstance(model, RANSACRegressor):
        return 'RANSACRegressor'
    if isinstance(model, GradientBoostingRegressor):
        return 'GradientBoostingRegressor'
    if isinstance(model, Lasso):
        return 'Lasso'
    if isinstance(model, ElasticNet):
        return 'ElasticNet'
    if isinstance(model, LassoLars):
        return 'LassoLars'
    if isinstance(model, OrthogonalMatchingPursuit):
        return 'OrthogonalMatchingPursuit'
    if isinstance(model, BayesianRidge):
        return 'BayesianRidge'
    if isinstance(model, ARDRegression):
        return 'ARDRegression'
    if isinstance(model, SGDRegressor):
        return 'SGDRegressor'
    if isinstance(model, PassiveAggressiveRegressor):
        return 'PassiveAggressiveRegressor'
    if isinstance(model, MiniBatchKMeans):
        return 'MiniBatchKMeans'
    if xgb_installed:
        if isinstance(model, XGBClassifier):
            return 'XGBClassifier'
        if isinstance(model, XGBRegressor):
            return 'XGBRegressor'
    if keras_installed:
        if isinstance(model, KerasRegressor):
            return 'DeepLearningRegressor'
        if isinstance(model, KerasClassifier):
            return 'DeepLearningClassifier'
    if lgb_installed:
        if isinstance(model, LGBMClassifier):
            return 'LGBMClassifier'
        if isinstance(model, LGBMRegressor):
            return 'LGBMRegressor'
