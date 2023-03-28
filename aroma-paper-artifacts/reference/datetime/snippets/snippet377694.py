import datetime
import os
import random
import sys
from quantile_ml import Predictor
from quantile_ml.utils_models import load_ml_model
import dill
import numpy as np
import pandas as pd
from nose.tools import assert_equal, assert_not_equal, with_setup
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import utils_testing as utils
from quantile_ml.utils_models import load_ml_model


def feature_learning_getting_single_predictions_classification(model_name=None):
    np.random.seed(0)
    (df_titanic_train, df_titanic_test) = utils.get_titanic_binary_classification_dataset()
    column_descriptions = {'survived': 'output', 'embarked': 'categorical', 'pclass': 'categorical'}
    ml_predictor = Predictor(type_of_estimator='classifier', column_descriptions=column_descriptions)
    (df_titanic_train, fl_data) = train_test_split(df_titanic_train, test_size=0.2)
    ml_predictor.train(df_titanic_train, model_names=model_name, feature_learning=True, fl_data=fl_data)
    file_name = ml_predictor.save(str(random.random()))
    saved_ml_pipeline = load_ml_model(file_name)
    os.remove(file_name)
    try:
        keras_file_name = (file_name[:(- 5)] + '_keras_deep_learning_model.h5')
        os.remove(keras_file_name)
    except:
        pass
    df_titanic_test_dictionaries = df_titanic_test.to_dict('records')
    predictions = []
    for row in df_titanic_test_dictionaries:
        predictions.append(saved_ml_pipeline.predict_proba(row)[1])
    print('predictions')
    print(predictions)
    first_score = utils.calculate_brier_score_loss(df_titanic_test.survived, predictions)
    print('first_score')
    print(first_score)
    lower_bound = (- 0.215)
    if (model_name == 'DeepLearningClassifier'):
        lower_bound = (- 0.25)
    if ((model_name == 'GradientBoostingClassifier') or (model_name is None)):
        lower_bound = (- 0.23)
    if (model_name == 'LGBMClassifier'):
        lower_bound = (- 0.221)
    if (model_name == 'XGBClassifier'):
        lower_bound = (- 0.245)
    assert (lower_bound < first_score < (- 0.17))
    data_length = len(df_titanic_test_dictionaries)
    start_time = datetime.datetime.now()
    for idx in range(1000):
        row_num = (idx % data_length)
        saved_ml_pipeline.predict(df_titanic_test_dictionaries[row_num])
    end_time = datetime.datetime.now()
    duration = (end_time - start_time)
    print('duration.total_seconds()')
    print(duration.total_seconds())
    assert (0.2 < duration.total_seconds() < 15)
    predictions = []
    for row in df_titanic_test_dictionaries:
        predictions.append(saved_ml_pipeline.predict_proba(row)[1])
    print('predictions')
    print(predictions)
    print('df_titanic_test_dictionaries')
    print(df_titanic_test_dictionaries)
    second_score = utils.calculate_brier_score_loss(df_titanic_test.survived, predictions)
    print('second_score')
    print(second_score)
    assert (lower_bound < second_score < (- 0.17))
