import pandas as pd
import numpy as np
import pickle


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = (int(((data_size - 1) / batch_size)) + 1)
    for epoch in range(num_epochs):
        if shuffle:
            np.random.seed(2017)
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = (batch_num * batch_size)
            end_index = min(((batch_num + 1) * batch_size), data_size)
            (yield shuffled_data[start_index:end_index])
