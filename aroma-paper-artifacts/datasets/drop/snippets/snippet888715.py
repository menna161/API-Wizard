import os
import numpy as np
import pandas as pd
from sklearn import preprocessing


def load_data(self):
    'Load, preprocess and class-balance the credit data.'
    rng = np.random.RandomState(self.seed)
    data = pd.read_csv(self.datapath, index_col=0)
    data.dropna(inplace=True)
    features = data.drop('SeriousDlqin2yrs', axis=1)
    features = preprocessing.scale(features)
    features = np.append(features, np.ones((features.shape[0], 1)), axis=1)
    outcomes = np.array(data['SeriousDlqin2yrs'])
    default_indices = np.where((outcomes == 1))[0]
    other_indices = np.where((outcomes == 0))[0][:10000]
    indices = np.concatenate((default_indices, other_indices))
    features_balanced = features[indices]
    outcomes_balanced = outcomes[indices]
    shape = features_balanced.shape
    shuffled = rng.permutation(len(indices))
    return (features_balanced[shuffled], outcomes_balanced[shuffled])
