import numpy as np
import scipy.sparse as sp


def train_test_split(X, train_size=0.75, random_state=None):
    cv = ShuffleSplit(n_iter=1, train_size=train_size, random_state=random_state)
    return next(cv.split(X))
