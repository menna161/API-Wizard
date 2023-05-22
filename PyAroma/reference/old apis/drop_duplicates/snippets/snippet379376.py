import pickle
import os
import time
import copy
from typing import List, Dict, Tuple
from pprint import pprint
import random
import pandas as pd
import numpy as np
from sklearn.model_selection import ParameterGrid
from models import LGBModel
from utils import save_float_mem, parse_time, generate_additional_num_features, get_lag_features, get_batch_id, cat_and_batch_id


def train(self, train_data: pd.DataFrame, time_info):
    t1 = time.time()
    print(f'''
Train time budget: {time_info['train']}s''')
    print('Train data shape:', train_data.shape, '\n\n')
    X = train_data.copy()
    X = save_float_mem(X)
    X = get_batch_id(X, self.dtype_cols['idd'])
    if (self.top_num_features is None):
        self.determine_important_features(X.drop(([self.label] + [self.primary_timestamp]), axis=1), X[self.label], topn=3)
    X = generate_additional_num_features(X, self.top_num_features)
    if (len(self.dtype_cols['idd']) != 0):
        self.batch_size = int(X[self.dtype_cols['idd']].drop_duplicates().shape[0])
        self.full_data = train_data.tail((self.batch_size * MAX_SHIFT))
    else:
        self.batch_size = 1
        self.full_data = train_data.tail((self.batch_size * MAX_SHIFT))
    print(f'''Batch size: {self.batch_size}

''')
    X = get_lag_features(X, [self.label], lags=TARGET_LAGS)
    X = get_lag_features(X, self.top_num_features, lags=FEATURES_LAGS)
    self.dtype_cols['cat'] = [col for col in X.columns if ((col in self.dtype_cols['cat']) or (X[col].dtype == np.dtype('object')))]
    X = cat_and_batch_id(X, self.dtype_cols['cat'])
    time_fea = parse_time(X[self.primary_timestamp])
    X = X.drop(self.primary_timestamp, axis=1)
    X = pd.concat([X, time_fea], axis=1)
    X = X.reset_index(drop=True)
    y = X[self.label].copy()
    X = X.drop(self.label, axis=1)
    self.train_columns = list(X.columns)
    self.columns_dtypes = X.dtypes
    t2 = time.time()
    print(f'Processing time: {(t2 - t1):.2f}')
    if (self.best_params is None):
        print(X.sample(10))
        for col in X.columns:
            print(col, len(set(X[col].dropna())), np.mean(X[col].isnull()))
        self.training_time_left = ((self.info['time_budget']['train'] * self.time_pillow_coef) - (t2 - t1))
        self.train_baseline(X, y)
        self.optimize_params(X, y)
        self.select_features(X, y)
        self.optimize_model_params(X, y)
        self.show_training_results()
    else:
        print(('\n\n' + ('-' * 60)))
        print('Refit model')
        pprint(self.best_params)
        print((('-' * 60) + '\n\n'))
        model = LGBModel(**self.best_params)
        model.fit(X, y)
        self.model = model
    if (self.update_interval is None):
        print(f'''Time for training: {self.time_for_training} s

''')
        n_retrain = np.ceil(((self.info['time_budget']['update'] / self.time_for_training) / self.training_time_coef))
        if (self.n_test_timestamp <= 1):
            n_retrain = 0
        else:
            n_retrain = np.clip(0, (self.n_test_timestamp - 1), n_retrain)
        self.n_retrain = int(n_retrain)
        if (self.n_retrain > 0):
            self.update_interval = np.ceil((self.n_test_timestamp / self.n_retrain))
            self.update_interval = int(self.update_interval)
        else:
            self.update_interval = np.inf
        print(f'''Num retraining: {n_retrain}

''')
    return 'predict'
