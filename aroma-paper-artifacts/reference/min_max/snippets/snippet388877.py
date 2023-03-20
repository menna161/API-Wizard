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


def get_merge_feature(df, feature_df, col_key, col_target, agg, sub='', scale=False):
    logger.info('df %s, col_key %s, col_target %s, agg %s, sub %s', df.shape, col_key, col_target, agg, sub)
    for ag in agg:
        new_col_names = f'{col_key}_{col_target}_w{sub}_{ag}'
        tmp_df = feature_df.groupby(col_key)[col_target].agg([ag]).reset_index().rename(columns={ag: new_col_names})
        tmp_df.index = list(tmp_df[col_key])
        if scale:
            scaler = MinMaxScaler()
            tmp_df[new_col_names] = scaler.fit_transform(tmp_df[new_col_names].values.reshape((- 1), 1))
        tmp_df = tmp_df[new_col_names].to_dict()
        df[new_col_names] = df[col_key].map(tmp_df).astype('float32')
        print(new_col_names, ', ', end='')
    return df
