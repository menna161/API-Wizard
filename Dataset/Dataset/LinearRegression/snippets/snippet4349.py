import numpy as np
from sklearn.linear_model import LinearRegression
import json as json
import sys


@staticmethod
def get_angle(xs, y_samples):
    (xs, ys) = (xs[(xs >= 0)], y_samples[(xs >= 0)])
    if (len(xs) > 1):
        LaneEval.lr.fit(ys[(:, None)], xs)
        k = LaneEval.lr.coef_[0]
        theta = np.arctan(k)
    else:
        theta = 0
    return theta
