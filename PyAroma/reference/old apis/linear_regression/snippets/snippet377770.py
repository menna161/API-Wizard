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


def get_model_from_name(model_name, training_params=None):
    epochs = 250
    if ((os.environ.get('is_test_suite', 0) == 'True') and (model_name[:12] == 'DeepLearning')):
        print('Heard that this is the test suite. Limiting number of epochs, which will increase training speed dramatically at the expense of model accuracy')
        epochs = 30
    all_model_params = {'LogisticRegression': {'n_jobs': (- 2)}, 'RandomForestClassifier': {'n_jobs': (- 2)}, 'ExtraTreesClassifier': {'n_jobs': (- 1)}, 'AdaBoostClassifier': {'n_estimators': 10}, 'SGDClassifier': {'n_jobs': (- 1)}, 'Perceptron': {'n_jobs': (- 1)}, 'LinearRegression': {'n_jobs': (- 2)}, 'RandomForestRegressor': {'n_jobs': (- 2)}, 'ExtraTreesRegressor': {'n_jobs': (- 1)}, 'MiniBatchKMeans': {'n_clusters': 8}, 'GradientBoostingRegressor': {'presort': False}, 'SGDRegressor': {'shuffle': False}, 'PassiveAggressiveRegressor': {'shuffle': False}, 'AdaBoostRegressor': {'n_estimators': 10}, 'XGBRegressor': {'nthread': (- 1), 'n_estimators': 200}, 'XGBClassifier': {'nthread': (- 1), 'n_estimators': 200}, 'LGBMRegressor': {}, 'LGBMClassifier': {}, 'DeepLearningRegressor': {'epochs': epochs, 'batch_size': 50, 'verbose': 2}, 'DeepLearningClassifier': {'epochs': epochs, 'batch_size': 50, 'verbose': 2}}
    model_params = all_model_params.get(model_name, None)
    if (model_params is None):
        model_params = {}
    if (training_params is not None):
        print('Now using the model training_params that you passed in:')
        print(training_params)
        model_params.update(training_params)
        print('After overwriting our defaults with your values, here are the final params that will be used to initialize the model:')
        print(model_params)
    model_map = {'LogisticRegression': LogisticRegression(), 'RandomForestClassifier': RandomForestClassifier(), 'RidgeClassifier': RidgeClassifier(), 'GradientBoostingClassifier': GradientBoostingClassifier(), 'ExtraTreesClassifier': ExtraTreesClassifier(), 'AdaBoostClassifier': AdaBoostClassifier(), 'SGDClassifier': SGDClassifier(), 'Perceptron': Perceptron(), 'PassiveAggressiveClassifier': PassiveAggressiveClassifier(), 'LinearRegression': LinearRegression(), 'RandomForestRegressor': RandomForestRegressor(), 'Ridge': Ridge(), 'ExtraTreesRegressor': ExtraTreesRegressor(), 'AdaBoostRegressor': AdaBoostRegressor(), 'RANSACRegressor': RANSACRegressor(), 'GradientBoostingRegressor': GradientBoostingRegressor(), 'Lasso': Lasso(), 'ElasticNet': ElasticNet(), 'LassoLars': LassoLars(), 'OrthogonalMatchingPursuit': OrthogonalMatchingPursuit(), 'BayesianRidge': BayesianRidge(), 'ARDRegression': ARDRegression(), 'SGDRegressor': SGDRegressor(), 'PassiveAggressiveRegressor': PassiveAggressiveRegressor(), 'MiniBatchKMeans': MiniBatchKMeans()}
    if xgb_installed:
        model_map['XGBClassifier'] = XGBClassifier()
        model_map['XGBRegressor'] = XGBRegressor()
    if lgb_installed:
        model_map['LGBMRegressor'] = LGBMRegressor()
        model_map['LGBMClassifier'] = LGBMClassifier()
    if keras_installed:
        model_map['DeepLearningClassifier'] = KerasClassifier(build_fn=make_deep_learning_classifier)
        model_map['DeepLearningRegressor'] = KerasRegressor(build_fn=make_deep_learning_model)
    try:
        model_without_params = model_map[model_name]
    except KeyError as e:
        print('It appears you are trying to use a library that is not available when we try to import it, or using a value for model_names that we do not recognize')
        raise e
    model_with_params = model_without_params.set_params(**model_params)
    return model_with_params
