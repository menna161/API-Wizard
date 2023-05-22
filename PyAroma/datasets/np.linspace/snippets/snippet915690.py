from __future__ import division
import numpy as np
from scipy.stats import gaussian_kde


def getinsidepoints(p1, p2, parts=2):
    'return: equally distanced points between starting and ending "control" points'
    return np.array((np.linspace(p1[0], p2[0], (parts + 1)), np.linspace(p1[1], p2[1], (parts + 1))))
