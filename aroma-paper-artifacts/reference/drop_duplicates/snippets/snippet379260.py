import pickle
import pandas as pd
import numpy as np
from models.lgb import LGBMRegressor
from models.rg import RidgeModel
from models.lasso import LassoModel
import os
import gc
from table import Table
from transform import CatTransformer, NumTransformer
from feature.feat_engine import FeatEngine
from feature.feat_pipeline import FeatPipeline
from autoeda import AutoEDA
from log_utils import log, timeit
import time
import math
from sklearn.metrics import mean_squared_error
import CONSTANT
from data_utils import trans_label, inverse_label, get_rmse


def train(self, train_data, time_info):
    t0 = time.time()
    print(f'''
Train time budget: {time_info['train']}s''')
    self.n_train += 1
    if (self.n_train == 1):
        X = train_data
        shape1 = X.shape
        print(f'shape1: {shape1}')
        X.drop_duplicates(keep='first', inplace=True)
        shape2 = X.shape
        print(f'shape1: {shape2}')
        self.preprocess(X, mode='fit_trans')
        self.table = Table(X, self.info)
    feat_pipline = FeatPipeline()
    feat_engine = FeatEngine(feat_pipline)
    feat_engine.fit_transform_oder1s(self.table)
    self.feat_engine = feat_engine
    (X, y, cat) = self.table.fit_transform_output()
    t1 = time.time()
    if (self.n_update == 0):
        do_explore = True
    else:
        do_explore = False
    time_left = (time_info['train'] - (t1 - t0))
    self.explore_space(X, y, cat, time_left, do_explore=do_explore)
    t2 = time.time()
    drop = []
    for (name, loader) in self.models.items():
        try:
            loader['model'].fit(X, y, cat)
        except:
            drop.append(name)
    for name in drop:
        self.models.pop(name)
    if (self.table.key_window is None):
        self.table.init_key_window()
    self.table.train_X = None
    self.table.train_y = None
    print('Finish train\n')
    next_step = 'predict'
    self.explore_duration = (t2 - t1)
    if (self.train_duration is None):
        self.train_duration = ((time.time() - t0) - self.explore_duration)
    max_update_num = (int((time_info['update'] / self.train_duration)) + 1)
    self.update_interval = ((self.n_test_timestamp - self.n_predict_true) / max_update_num)
    return next_step
