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


def getting_single_predictions_multilabel_classification(model_name=None):
    if (model_name == 'DeepLearningClassifier'):
        return
    np.random.seed(0)
    (df_twitter_train, df_twitter_test) = utils.get_twitter_sentiment_multilabel_classification_dataset()
    column_descriptions = {'airline_sentiment': 'output', 'airline': 'categorical', 'text': 'ignore', 'tweet_location': 'categorical', 'user_timezone': 'categorical', 'tweet_created': 'date'}
    ml_predictor = Predictor(type_of_estimator='classifier', column_descriptions=column_descriptions)
    ml_predictor.train(df_twitter_train, model_names=model_name)
    file_name = ml_predictor.save(str(random.random()))
    saved_ml_pipeline = load_ml_model(file_name)
    os.remove(file_name)
    try:
        keras_file_name = (file_name[:(- 5)] + '_keras_deep_learning_model.h5')
        os.remove(keras_file_name)
    except:
        pass
    df_twitter_test_dictionaries = df_twitter_test.to_dict('records')
    predictions = []
    for row in df_twitter_test_dictionaries:
        predictions.append(saved_ml_pipeline.predict(row))
    print('predictions')
    print(predictions)
    first_score = accuracy_score(df_twitter_test.airline_sentiment, predictions)
    print('first_score')
    print(first_score)
    lower_bound = 0.67
    if (model_name == 'LGBMClassifier'):
        lower_bound = 0.655
    assert (lower_bound < first_score < 0.79)
    data_length = len(df_twitter_test_dictionaries)
    start_time = datetime.datetime.now()
    for idx in range(1000):
        row_num = (idx % data_length)
        saved_ml_pipeline.predict(df_twitter_test_dictionaries[row_num])
    end_time = datetime.datetime.now()
    duration = (end_time - start_time)
    print('duration.total_seconds()')
    print(duration.total_seconds())
    assert (0.2 < duration.total_seconds() < 15)
    predictions = []
    for row in df_twitter_test_dictionaries:
        predictions.append(saved_ml_pipeline.predict(row))
    print('predictions')
    print(predictions)
    print('df_twitter_test_dictionaries')
    print(df_twitter_test_dictionaries)
    second_score = accuracy_score(df_twitter_test.airline_sentiment, predictions)
    print('second_score')
    print(second_score)
    assert (lower_bound < second_score < 0.79)
