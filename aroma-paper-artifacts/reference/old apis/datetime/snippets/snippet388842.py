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


def configure_logging(filename):
    if (len(filename) < 10):
        log_filename = ((f'{filename}_' + datetime.datetime.now().strftime('%Y-%m-%d')) + '.log')
    else:
        log_filename = filename
    log_fmt = '[%(asctime)s] %(funcName)s: %(message)s'
    formatter = logging.Formatter(log_fmt)
    fh = logging.FileHandler(filename=os.path.join('../logs', log_filename))
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger = logging.getLogger(filename)
    logger.setLevel(logging.INFO)
    logger.addHandler(fh)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger
