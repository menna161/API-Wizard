import logging
import random
import threading
from datetime import datetime
import numpy as np
from scipy import sparse
from sklearn.preprocessing import MinMaxScaler
from .utils import Indexer, create_sparse, timestamp_delta_generator


def sample_generator(usr_rates_movies_ds, observation_begin, observation_end, rate_sparse, indexer, censoring_ratio):
    logging.info('generating samples ...')
    U_M = rate_sparse
    observed_samples = {}
    for line in usr_rates_movies_ds[1:]:
        line_items = line.split('\t')
        rating = float(line_items[2])
        rating_timestamp = (float(line_items[3]) / 1000)
        if ((observation_begin < rating_timestamp <= observation_end) and (rating > rating_threshold)):
            u = indexer.get_index('user', line_items[0])
            v = indexer.get_index('movie', line_items[1])
            if (not ((u is None) or (v is None))):
                observed_samples[(u, v)] = (rating_timestamp - observation_begin)
    nonzero = sparse.find(U_M)
    set_observed = set(([(u, v) for (u, v) in observed_samples] + [(u, v) for (u, v) in zip(nonzero[0], nonzero[1])]))
    censored_samples = {}
    M = (len(observed_samples) // ((1 / censoring_ratio) - 1))
    user_list = [i for i in range(U_M.shape[0])]
    movie_list = [i for i in range(U_M.shape[1])]
    while (len(censored_samples) < M):
        i = random.randint(0, (len(user_list) - 1))
        j = random.randint(0, (len(movie_list) - 1))
        if (i != j):
            u = user_list[i]
            v = movie_list[j]
            if ((u, v) not in set_observed):
                censored_samples[(u, v)] = ((observation_end - observation_begin) + 1)
    return (observed_samples, censored_samples)
