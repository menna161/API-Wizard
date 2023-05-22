import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
import logging
import joblib
import datetime
import sys
import collections
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import itertools
import time
import multiprocessing
from sklearn.preprocessing import MinMaxScaler
import warnings
from sklearn import metrics
from functools import wraps
import wrapt
import random
import tarfile
import zipfile


@timeit
def get_key1_feature(df, key1, target, agg, sub='', ret_dict=False, scale=False):
    t = df.groupby([key1])[target].agg(agg).reset_index()
    cols = []
    for a in agg:
        cols.append(f'{key1}_{target}_w{sub}_{a}')
    t.columns = ([key1] + cols)
    logger.info('columns %s', t.columns.values.tolist())
    if scale:
        scaler = MinMaxScaler()
        for col in t.columns:
            if (key1 == col):
                continue
            t[col] = scaler.fit_transform(t[col].values.reshape((- 1), 1))
    if ret_dict:
        t = t.set_index(key1).to_dict()
    return t
