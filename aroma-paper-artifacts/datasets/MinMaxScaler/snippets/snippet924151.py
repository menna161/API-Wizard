import logging
import random
import threading
from datetime import datetime
import numpy as np
from scipy import sparse
from sklearn.preprocessing import MinMaxScaler
from .utils import Indexer, create_sparse, timestamp_delta_generator


def run(delta, observation_window, n_snapshots, censoring_ratio=0.5, single_snapshot=False):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s', datefmt='%H:%M:%S')
    with open('data/delicious/user_contacts-timestamps.dat') as usr_usr:
        usr_dataset = usr_usr.read().splitlines()
    with open('data/delicious/user_taggedbookmarks-timestamps.dat') as usr_bm_tg:
        usr_bm_tg_dataset = usr_bm_tg.read().splitlines()
    delta = timestamp_delta_generator(months=delta)
    observation_end = datetime(2010, 10, 1).timestamp()
    observation_begin = (observation_end - timestamp_delta_generator(months=observation_window))
    feature_end = observation_begin
    feature_begin = (feature_end - (n_snapshots * delta))
    indexer = generate_indexer(usr_dataset, usr_bm_tg_dataset, feature_begin, feature_end)
    (contact_sparse, save_sparse, attach_sparse) = parse_dataset(usr_dataset, usr_bm_tg_dataset, feature_begin, feature_end, indexer)
    (observed_samples, censored_samples) = sample_generator(usr_dataset, observation_begin, observation_end, contact_sparse, indexer, censoring_ratio)
    (X, Y, T) = extract_features(contact_sparse, save_sparse, attach_sparse, observed_samples, censored_samples)
    X_list = [X]
    if (not single_snapshot):
        for t in range(int((feature_end - delta)), int(feature_begin), (- int(delta))):
            (contact_sparse, save_sparse, attach_sparse) = parse_dataset(usr_dataset, usr_bm_tg_dataset, feature_begin, t, indexer)
            (X, _, _) = extract_features(contact_sparse, save_sparse, attach_sparse, observed_samples, censored_samples)
            X_list = ([X] + X_list)
        for i in range(1, len(X_list)):
            X_list[i] -= X_list[(i - 1)]
    scaler = MinMaxScaler(copy=False)
    for X in X_list:
        scaler.fit_transform(X)
    X = np.stack(X_list, axis=1)
    T /= delta
    return (X, Y, T)
