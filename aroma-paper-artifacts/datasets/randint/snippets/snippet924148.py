import logging
import random
import threading
from datetime import datetime
import numpy as np
from scipy import sparse
from sklearn.preprocessing import MinMaxScaler
from .utils import Indexer, create_sparse, timestamp_delta_generator


def sample_generator(usr_dataset, observation_begin, observation_end, contact_sparse, indexer, censoring_ratio):
    logging.info('generating samples ...')
    U_U = contact_sparse.dot(contact_sparse.T)
    observed_samples = {}
    for line in usr_dataset[1:]:
        line_items = line.split('\t')
        contact_timestamp = (float(line_items[2]) / 1000)
        if (observation_begin < contact_timestamp <= observation_end):
            u = indexer.get_index('user', line_items[0])
            v = indexer.get_index('user', line_items[1])
            if (not ((u is None) or (v is None))):
                observed_samples[(u, v)] = (contact_timestamp - observation_begin)
    nonzero = sparse.find(U_U)
    set_observed = set(([(u, v) for (u, v) in observed_samples] + [(u, v) for (u, v) in zip(nonzero[0], nonzero[1])]))
    censored_samples = {}
    N = U_U.shape[0]
    M = (len(observed_samples) // ((1 / censoring_ratio) - 1))
    user_list = [i for i in range(N)]
    while (len(censored_samples) < M):
        i = random.randint(0, (len(user_list) - 1))
        j = random.randint(0, (len(user_list) - 1))
        if (i != j):
            u = user_list[i]
            v = user_list[j]
            if ((u, v) not in set_observed):
                censored_samples[(u, v)] = ((observation_end - observation_begin) + 1)
    return (observed_samples, censored_samples)
