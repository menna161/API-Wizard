import os
from sklearn.externals.joblib import load
from modl.utils.recsys.cross_validation import train_test_split
from modl.datasets import get_data_dirs


def load_recsys(dataset, random_state):
    if (dataset in ['100k', '1m', '10m']):
        X = load_movielens(dataset)
        (X_tr, X_te) = train_test_split(X, train_size=0.75, random_state=random_state)
        X_tr = X_tr.tocsr()
        X_te = X_te.tocsr()
        return (X_tr, X_te)
    if (dataset is 'netflix'):
        return load_netflix()
