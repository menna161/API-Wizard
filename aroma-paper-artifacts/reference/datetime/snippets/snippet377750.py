import datetime
import dill
from nose.tools import raises
import numpy as np
import os
import random
import sys
import warnings
from quantile_ml import Predictor
import utils_testing as utils


def test_unexpected_datetime_column_handled_without_errors():
    (df_titanic_train, df_titanic_test) = utils.get_titanic_binary_classification_dataset()
    column_descriptions = {'survived': 'output', 'embarked': 'categorical', 'pclass': 'categorical'}
    ml_predictor = Predictor(type_of_estimator='classifier', column_descriptions=column_descriptions)
    ml_predictor.train(df_titanic_train)
    test_dict = df_titanic_test.sample(frac=0.1).to_dict('records')[0]
    test_dict['unexpected_column'] = datetime.date.today()
    test_dict['anoter_unexpected_column'] = datetime.datetime.today()
    ml_predictor.predict(test_dict)
    assert True
