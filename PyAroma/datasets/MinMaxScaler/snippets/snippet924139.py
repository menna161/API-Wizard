import bisect
import logging
import random
import threading
import Stemmer
import numpy as np
import nltk
from sklearn.preprocessing import MinMaxScaler
from nltk.corpus import stopwords as stop_words
from scipy import sparse
from .utils import Indexer, create_sparse


def run(delta, observation_window, n_snapshots, censoring_ratio=0.5, single_snapshot=False):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s', datefmt='%H:%M:%S')
    conf_list = {'db': ['KDD', 'PKDD', 'ICDM', 'SDM', 'PAKDD', 'SIGMOD', 'VLDB', 'ICDE', 'PODS', 'EDBT', 'SIGIR', 'ECIR', 'ACL', 'WWW', 'CIKM', 'NIPS', 'ICML', 'ECML', 'AAAI', 'IJCAI'], 'th': ['STOC', 'FOCS', 'COLT', 'LICS', 'SCG', 'SODA', 'SPAA', 'PODC', 'ISSAC', 'CRYPTO', 'EUROCRYPT', 'CONCUR', 'ICALP', 'STACS', 'COCO', 'WADS', 'MFCS', 'SWAT', 'ESA', 'IPCO', 'LFCS', 'ALT', 'EUROCOLT', 'WDAG', 'ISTCS', 'FSTTCS', 'LATIN', 'RECOMB', 'CADE', 'ISIT', 'MEGA', 'ASIAN', 'CCCG', 'FCT', 'WG', 'CIAC', 'ICCI', 'CATS', 'COCOON', 'GD', 'ISAAC', 'SIROCCO', 'WEA', 'ALENEX', 'FTP', 'CSL', 'DMTCS']}[path]
    observation_end = 2016
    observation_begin = (observation_end - observation_window)
    feature_end = observation_begin
    feature_begin = (feature_end - (delta * n_snapshots))
    (papers_feat_window, papers_obs_window, counter) = generate_papers('data/dblp/dblp.txt', feature_begin, feature_end, observation_begin, observation_end, conf_list)
    (W, C, I, P) = parse_dataset(papers_feat_window, feature_begin, feature_end, counter)
    (observed_samples, censored_samples) = generate_samples(papers_obs_window, censoring_ratio, W, C)
    (X, Y, T) = extract_features(W, C, P, I, observed_samples, censored_samples)
    X_list = [X]
    if (not single_snapshot):
        for t in range((feature_end - delta), feature_begin, (- delta)):
            (W, C, I, P) = parse_dataset(papers_feat_window, feature_begin, t, counter)
            (X, _, _) = extract_features(W, C, P, I, observed_samples, censored_samples)
            X_list = ([X] + X_list)
        for i in range(1, len(X_list)):
            X_list[i] -= X_list[(i - 1)]
    scaler = MinMaxScaler(copy=False)
    for X in X_list:
        scaler.fit_transform(X)
    X = np.stack(X_list, axis=1)
    T = (T - observation_begin)
    return (X, Y, T)
