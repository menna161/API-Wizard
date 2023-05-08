from math import floor
from copy import deepcopy
from utils.MathUtil import *
from sklearn.preprocessing import MinMaxScaler


def _preprocessing_2d__(self):
    '\n            output_index = None\n                + single input => single output\n                + multiple input => multiple output\n\n            output_index = number (index)\n                + single input => single output index\n                + multiple input => single output index\n\n            valid_idx = 0 ==> No validate data ||  cpu(t), cpu(t-1), ..., ram(t), ram(t-1),...\n        '
    if (self.output_index is None):
        list_transform = self.minmax_scaler.fit_transform(self.original_dataset)
        dataset_y = deepcopy(list_transform[self.sliding:])
    else:
        list_transform = np.zeros(shape=(self.original_dataset_len, 1))
        for i in range(0, self.dimension):
            t = ((self.output_index - (self.dimension - 1)) + i)
            d1 = self.minmax_scaler.fit_transform(self.original_dataset[(:self.original_dataset_len, t)].reshape((- 1), 1))
            list_transform = np.concatenate((list_transform, d1), axis=1)
        list_transform = list_transform[(:, 1:)]
        dataset_y = deepcopy(list_transform[(self.sliding:, (- 1):)])
    dataset_X = self.__get_dataset_X__(list_transform)
    if (self.valid_len == 0):
        (X_train, y_train) = (dataset_X[0:self.train_idx], dataset_y[0:self.train_idx])
        (X_test, y_test) = (dataset_X[self.train_idx:self.test_idx], dataset_y[self.train_idx:self.test_idx])
        return (X_train, y_train, None, None, X_test, y_test)
    else:
        (X_train, y_train) = (dataset_X[0:self.train_idx], dataset_y[0:self.train_idx])
        (X_valid, y_valid) = (dataset_X[self.train_idx:self.valid_idx], dataset_y[self.train_idx:self.valid_idx])
        (X_test, y_test) = (dataset_X[self.valid_idx:self.test_idx], dataset_y[self.valid_idx:self.test_idx])
        return (X_train, y_train, X_valid, y_valid, X_test, y_test)
