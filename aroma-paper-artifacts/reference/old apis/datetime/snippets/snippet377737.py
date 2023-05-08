import datetime
import os
import random
import sys
from quantile_ml import Predictor
from quantile_ml.utils_models import load_ml_model
import dill
from nose.tools import assert_equal, assert_not_equal, with_setup
import numpy as np
from sklearn.model_selection import train_test_split
import utils_testing as utils
from quantile_ml.utils_models import load_ml_model


def feature_learning_getting_single_predictions_regression(model_name=None):
    np.random.seed(0)
    (df_boston_train, df_boston_test) = utils.get_boston_regression_dataset()
    column_descriptions = {'MEDV': 'output', 'CHAS': 'categorical'}
    ml_predictor = Predictor(type_of_estimator='regressor', column_descriptions=column_descriptions)
    (df_boston_train, fl_data) = train_test_split(df_boston_train, test_size=0.2)
    ml_predictor.train(df_boston_train, model_names=model_name, feature_learning=True, fl_data=fl_data)
    file_name = ml_predictor.save(str(random.random()))
    saved_ml_pipeline = load_ml_model(file_name)
    os.remove(file_name)
    try:
        keras_file_name = (file_name[:(- 5)] + '_keras_deep_learning_model.h5')
        os.remove(keras_file_name)
    except:
        pass
    df_boston_test_dictionaries = df_boston_test.to_dict('records')
    predictions = []
    for row in df_boston_test_dictionaries:
        predictions.append(saved_ml_pipeline.predict(row))
    first_score = utils.calculate_rmse(df_boston_test.MEDV, predictions)
    print('first_score')
    print(first_score)
    lower_bound = (- 3.2)
    if (model_name == 'DeepLearningRegressor'):
        lower_bound = (- 23)
    if (model_name == 'LGBMRegressor'):
        lower_bound = (- 4.95)
    if (model_name == 'XGBRegressor'):
        lower_bound = (- 3.3)
    assert (lower_bound < first_score < (- 2.8))
    data_length = len(df_boston_test_dictionaries)
    start_time = datetime.datetime.now()
    for idx in range(1000):
        row_num = (idx % data_length)
        saved_ml_pipeline.predict(df_boston_test_dictionaries[row_num])
    end_time = datetime.datetime.now()
    duration = (end_time - start_time)
    print('duration.total_seconds()')
    print(duration.total_seconds())
    assert (0.2 < (duration.total_seconds() / 1.0) < 15)
    predictions = []
    for row in df_boston_test_dictionaries:
        predictions.append(saved_ml_pipeline.predict(row))
    second_score = utils.calculate_rmse(df_boston_test.MEDV, predictions)
    print('second_score')
    print(second_score)
    assert (lower_bound < second_score < (- 2.8))
