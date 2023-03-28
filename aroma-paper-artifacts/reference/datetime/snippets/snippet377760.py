import datetime
import dateutil
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings


def add_date_features_dict(row, date_col):
    date_feature_dict = {}
    try:
        date_val = row[date_col]
        if (date_val == None):
            return date_feature_dict
        if (not isinstance(date_val, (datetime.datetime, datetime.date))):
            date_val = dateutil.parser.parse(date_val)
    except:
        return date_feature_dict
    date_feature_dict[(date_col + '_day_of_week')] = date_val.weekday()
    try:
        date_feature_dict[(date_col + '_hour')] = date_val.hour
        date_feature_dict[(date_col + '_minutes_into_day')] = ((date_val.hour * 60) + date_val.minute)
    except AttributeError:
        pass
    date_feature_dict[(date_col + '_is_weekend')] = (date_val.weekday() in (5, 6))
    return date_feature_dict
