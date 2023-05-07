import logging
import numpy as np
from sklearn.model_selection import train_test_split
from models import Model
from models import optimize


@staticmethod
def loss(w, X, Y, H):
    '\n        negative log likelihood (complete)\n        refer to formulations of NP-GLM\n        '
    Xw = np.dot(X, w)
    E = np.exp(Xw)
    HE = (H * E)
    p = (X * (HE - Y)[(:, None)])
    f = np.sum((HE - (Y * Xw)), axis=0)
    g = np.sum(p, axis=0)
    h = np.dot(X.T, (X * HE[(:, None)]))
    return (f, g, h)
