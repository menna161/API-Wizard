import datetime
import os
import random
import sys
from quantile_ml import Predictor
from nose.tools import assert_equal, assert_not_equal, with_setup
from sklearn.metrics import accuracy_score
import dill
import numpy as np
import utils_testing as utils


def test_all_algos_regression():
    np.random.seed(0)
    (df_boston_train, df_boston_test) = utils.get_boston_regression_dataset()
    column_descriptions = {'MEDV': 'output', 'CHAS': 'categorical'}
    ml_predictor = Predictor(type_of_estimator='regressor', column_descriptions=column_descriptions)
    ml_predictor.train(df_boston_train, model_names=['LinearRegression', 'RandomForestRegressor', 'Ridge', 'GradientBoostingRegressor', 'ExtraTreesRegressor', 'AdaBoostRegressor', 'SGDRegressor', 'PassiveAggressiveRegressor', 'Lasso', 'LassoLars', 'ElasticNet', 'OrthogonalMatchingPursuit', 'BayesianRidge', 'ARDRegression', 'MiniBatchKMeans', 'DeepLearningRegressor'])
    test_score = ml_predictor.score(df_boston_test, df_boston_test.MEDV)
    print('test_score')
    print(test_score)
    assert ((- 3.35) < test_score < (- 2.8))
