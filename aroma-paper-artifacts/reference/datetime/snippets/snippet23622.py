import pandas as pd
import numpy as np
import io
import requests
from datetime import timedelta
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import *
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn


def prepare_data(self, df, fill=False):
    df = df.set_index('Date')
    df['Year'] = df.index.year
    df['Month'] = df.index.month
    df['Week'] = df.index.week
    df['DOW'] = df.index.weekday
    yearly_avg = dict(df.groupby('Year')['Value'].mean())
    df['year_avg'] = df['Year'].apply((lambda x: yearly_avg[x]))
    monthly_avg = dict(df.groupby('Month')['Value'].mean())
    df['month_avg'] = df['Month'].apply((lambda x: monthly_avg[x]))
    weekly_avg = dict(df.groupby('Week')['Value'].mean())
    df['week_avg'] = df['Week'].apply((lambda x: weekly_avg[x]))
    dow_avg = dict(df.groupby('DOW')['Value'].mean())
    df['dow_avg'] = df['DOW'].apply((lambda x: dow_avg[x]))
    df = df.drop(['Year', 'Month', 'Week', 'DOW'], axis=1)
    start_date = pd.to_datetime(self.predicted_date).date()
    end_date = (start_date + timedelta(days=6))
    train = df.loc[(df.index.date < start_date)]
    train = ForecastRunner.remove_outliers(train, fill)
    test = df.loc[((df.index.date >= start_date) & (df.index.date <= end_date))]
    return (train, test)
