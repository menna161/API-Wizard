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


def test_is_backwards_compatible_with_models_trained_using_1_9_6():
    np.random.seed(0)
    (df_boston_train, df_boston_test) = utils.get_boston_regression_dataset()
    with open(os.path.join('tests', 'trained_ml_model_v_1_9_6.dill'), 'rb') as read_file:
        saved_ml_pipeline = dill.load(read_file)
    df_boston_test_dictionaries = df_boston_test.to_dict('records')
    predictions = []
    for row in df_boston_test_dictionaries:
        predictions.append(saved_ml_pipeline.predict(row))
    print('predictions')
    print(predictions)
    print('predictions[0]')
    print(predictions[0])
    print('type(predictions)')
    print(type(predictions))
    first_score = utils.calculate_rmse(df_boston_test.MEDV, predictions)
    print('first_score')
    print(first_score)
    assert ((- 2.8) < first_score < (- 2.1))
    data_length = len(df_boston_test_dictionaries)
    start_time = datetime.datetime.now()
    for idx in range(1000):
        row_num = (idx % data_length)
        saved_ml_pipeline.predict(df_boston_test_dictionaries[row_num])
    end_time = datetime.datetime.now()
    duration = (end_time - start_time)
    print('duration.total_seconds()')
    print(duration.total_seconds())
    assert (0.1 < (duration.total_seconds() / 1.0) < 15)
    predictions = []
    for row in df_boston_test_dictionaries:
        predictions.append(saved_ml_pipeline.predict(row))
    second_score = utils.calculate_rmse(df_boston_test.MEDV, predictions)
    print('second_score')
    print(second_score)
    assert ((- 2.8) < second_score < (- 2.1))
