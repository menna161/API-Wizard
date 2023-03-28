import sys, os
import pandas as pd
from sklearn.datasets import load_boston
from sklearn.metrics import brier_score_loss, mean_squared_error
from sklearn.model_selection import train_test_split
from quantile_ml import Predictor


def get_twitter_sentiment_multilabel_classification_dataset():
    file_name = os.path.join('tests', 'twitter_sentiment.csv')
    try:
        df_twitter = pd.read_csv(open(file_name, 'rU'), encoding='utf-8', engine='python')
    except Exception as e:
        print('Error')
        print(e)
        dataset_url = 'https://raw.githubusercontent.com/ClimbsRocks/sample_datasets/master/twitter_airline_sentiment.csv'
        df_twitter = pd.read_csv(dataset_url)
        df_twitter.to_csv(file_name, index=False)
    df_twitter = df_twitter.sample(frac=0.1)
    df_twitter['tweet_created'] = pd.to_datetime(df_twitter.tweet_created)
    (df_twitter_train, df_twitter_test) = train_test_split(df_twitter, test_size=0.33, random_state=42)
    return (df_twitter_train, df_twitter_test)
