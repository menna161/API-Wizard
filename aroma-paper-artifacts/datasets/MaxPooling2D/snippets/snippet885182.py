import numpy as np
import random as rand
import math
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization


def best_genome(self, csv_path, metric='accuracy', include_metrics=True):
    best = (max if (metric is 'accuracy') else min)
    col = ((- 1) if (metric is 'accuracy') else (- 2))
    data = np.genfromtxt(csv_path, delimiter=',')
    row = list(data[(:, col)]).index(best(data[(:, col)]))
    genome = list(map(int, data[(row, :(- 2))]))
    if include_metrics:
        genome += list(data[(row, (- 2):)])
    return genome
