import pandas as pd
from sklearn.preprocessing import LabelEncoder


def fit_transform(self, X, y=None):
    return self.fit(X, y).transform(X)
