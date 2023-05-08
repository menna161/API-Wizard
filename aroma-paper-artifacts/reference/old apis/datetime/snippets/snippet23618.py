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


def get_input(self):
    s = requests.get(self.url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')), header=1)
    df['Value'] = df.drop(['Date', 'Values'], axis=1).sum(axis=1)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    input_data = df[['Date', 'Value']]
    return input_data
