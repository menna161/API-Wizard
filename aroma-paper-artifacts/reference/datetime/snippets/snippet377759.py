import datetime
import dateutil
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings


def add_date_features_df(df, date_col):
    df.is_copy = False
    df[date_col] = pd.to_datetime(df[date_col])
    df[(date_col + '_day_of_week')] = df[date_col].apply((lambda x: x.weekday())).astype(int, raise_on_error=False)
    try:
        df[(date_col + '_hour')] = df[date_col].apply((lambda x: x.hour)).astype(int, raise_on_error=False)
        df[(date_col + '_minutes_into_day')] = df[date_col].apply((lambda x: ((x.hour * 60) + x.minute)))
    except AttributeError:
        pass
    df[(date_col + '_is_weekend')] = df[date_col].apply((lambda x: (x.weekday() in (5, 6))))
    df[(date_col + '_day_part')] = df[(date_col + '_minutes_into_day')].apply(minutes_into_day_parts)
    df = df.drop([date_col], axis=1)
    return df
