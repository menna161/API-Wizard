import pandas as pd
import os
import numpy as np
import re
from sklearn.utils import shuffle
from collections import OrderedDict


def _split_data(x_data, y_data=None, train_ratio=0, split_type='uniform'):
    if ((split_type == 'uniform') and (y_data is not None)):
        pos_idx = (y_data > 0)
        x_pos = x_data[pos_idx]
        y_pos = y_data[pos_idx]
        x_neg = x_data[(~ pos_idx)]
        y_neg = y_data[(~ pos_idx)]
        train_pos = int((train_ratio * x_pos.shape[0]))
        train_neg = int((train_ratio * x_neg.shape[0]))
        x_train = np.hstack([x_pos[0:train_pos], x_neg[0:train_neg]])
        y_train = np.hstack([y_pos[0:train_pos], y_neg[0:train_neg]])
        x_test = np.hstack([x_pos[train_pos:], x_neg[train_neg:]])
        y_test = np.hstack([y_pos[train_pos:], y_neg[train_neg:]])
    elif (split_type == 'sequential'):
        num_train = int((train_ratio * x_data.shape[0]))
        x_train = x_data[0:num_train]
        x_test = x_data[num_train:]
        if (y_data is None):
            y_train = None
            y_test = None
        else:
            y_train = y_data[0:num_train]
            y_test = y_data[num_train:]
    indexes = shuffle(np.arange(x_train.shape[0]))
    x_train = x_train[indexes]
    if (y_train is not None):
        y_train = y_train[indexes]
    return ((x_train, y_train), (x_test, y_test))
