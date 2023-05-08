from math import floor
from copy import deepcopy
from utils.MathUtil import *
from sklearn.preprocessing import MinMaxScaler


def __get_dataset_X__(self, list_transform=None):
    '\n        :param list_transform: [ x1 | t1 ] => Make a window slides\n        :return: dataset_sliding = [ x1 | x2 | x3| t1 | t2 | t3 | ... ]\n        '
    dataset_sliding = np.zeros(shape=(self.test_idx, 1))
    for i in range(self.dimension):
        for j in range(self.sliding):
            temp = np.array(list_transform[(j:(self.test_idx + j), i:(i + 1))])
            dataset_sliding = np.concatenate((dataset_sliding, temp), axis=1)
    dataset_sliding = dataset_sliding[(:, 1:)]
    if (self.method_statistic == 0):
        dataset_X = deepcopy(dataset_sliding)
    else:
        dataset_X = np.zeros(shape=(self.test_idx, 1))
        if (self.method_statistic == 1):
            '\n                mean(x1, x2, x3, ...), mean(t1, t2, t3,...) \n                '
            for i in range(self.dimension):
                meanx = np.reshape(np.mean(dataset_sliding[(:, (i * self.sliding):((i + 1) * self.sliding))], axis=1), ((- 1), 1))
                dataset_X = np.concatenate((dataset_X, meanx), axis=1)
        if (self.method_statistic == 2):
            '\n                min(x1, x2, x3, ...), mean(x1, x2, x3, ...), max(x1, x2, x3, ....)\n                '
            for i in range(self.dimension):
                minx = np.reshape(np.amin(dataset_sliding[(:, (i * self.sliding):((i + 1) * self.sliding))], axis=1), ((- 1), 1))
                meanx = np.reshape(np.mean(dataset_sliding[(:, (i * self.sliding):((i + 1) * self.sliding))], axis=1), ((- 1), 1))
                maxx = np.reshape(np.amax(dataset_sliding[(:, (i * self.sliding):((i + 1) * self.sliding))], axis=1), ((- 1), 1))
                dataset_X = np.concatenate((dataset_X, minx, meanx, maxx), axis=1)
        if (self.method_statistic == 3):
            '\n                min(x1, x2, x3, ...), median(x1, x2, x3, ...), max(x1, x2, x3, ....), min(t1, t2, t3, ...), median(t1, t2, t3, ...), max(t1, t2, t3, ....)\n                '
            for i in range(self.dimension):
                minx = np.reshape(np.amin(dataset_sliding[(:, (i * self.sliding):((i + 1) * self.sliding))], axis=1), ((- 1), 1))
                medix = np.reshape(np.median(dataset_sliding[(:, (i * self.sliding):((i + 1) * self.sliding))], axis=1), ((- 1), 1))
                maxx = np.reshape(np.amax(dataset_sliding[(:, (i * self.sliding):((i + 1) * self.sliding))], axis=1), ((- 1), 1))
                dataset_X = np.concatenate((dataset_X, minx, medix, maxx), axis=1)
        dataset_X = dataset_X[(:, 1:)]
    if (self.expand_function is None):
        return dataset_X
    return ExpandingFunctions(dataset_X, self.expand_function).expand_data()
