from math import floor
from copy import deepcopy
from utils.MathUtil import *
from sklearn.preprocessing import MinMaxScaler


def __init__(self, dataset=None, data_idx=None, sliding=None, expand_function=None, output_index=None, method_statistic=0):
    '\n        :param data_idx:\n        :param sliding:\n        :param output_index:\n        :param method_statistic:\n        :param minmax_scaler:\n        '
    self.original_dataset = dataset
    self.dimension = dataset.shape[1]
    self.original_dataset_len = len(dataset)
    self.dataset_len = (self.original_dataset_len - sliding)
    self.train_idx = int((data_idx[0] * self.dataset_len))
    self.train_len = self.train_idx
    self.valid_idx = (self.train_idx + int((data_idx[1] * self.dataset_len)))
    self.valid_len = (self.valid_idx - self.train_idx)
    self.test_idx = self.dataset_len
    self.test_len = ((self.dataset_len - self.train_len) - self.valid_len)
    self.sliding = sliding
    self.expand_function = expand_function
    self.output_index = output_index
    self.method_statistic = method_statistic
    self.minmax_scaler = MinMaxScaler()
