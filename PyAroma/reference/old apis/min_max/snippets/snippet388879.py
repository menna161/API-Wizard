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
def get_key2_feature(df, key1, key2, target_col, agg, sub='', scale=False):
    t = df.groupby([key1, key2])[target_col].agg(agg).reset_index()
    cols = []
    for a in agg:
        cols.append(f'{key1}_{key2}_{target_col}_w{sub}_{a}')
    t.columns = ([key1, key2] + cols)
    if scale:
        scaler = MinMaxScaler()
        for col in t.columns:
            if (key1 == col):
                continue
            t[col] = scaler.fit_transform(t[col].values.reshape((- 1), 1))
    return t
