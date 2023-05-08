import pandas as pd
from sklearn.preprocessing import LabelEncoder


def transform(self, X):
    '\n        Transforms columns of X specified in self.columns using\n        LabelEncoder(). If no columns specified, transforms all\n        columns in X.\n        '
    output = X.copy()
    if (self.columns is not None):
        for col in self.columns:
            output[col] = LabelEncoder().fit_transform(output[col])
    else:
        for (colname, col) in output.iteritems():
            output[colname] = LabelEncoder().fit_transform(col)
    return output
