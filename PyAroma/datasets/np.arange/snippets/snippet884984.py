import sys
import numpy as np
from numpy import hypot, sqrt
from scipy.optimize import curve_fit
import sklearn
from astroML.density_estimation import bayesian_blocks
import matplotlib.pyplot as pl


def centroid(images):
    'Dumb dumb centroiding.  assumes x and y axes are the\n    last two dimensions of images.  Something is wrong with the\n    broadcasting.  absolutely *have* to include weighting'
    sz = images.shape[(- 2):]
    xg = np.arange(sz[0])
    yg = np.arange(sz[1])
    denom = images.sum(axis=((- 1), (- 2)))
    y = ((yg[(None, None, :)] * images).sum(axis=((- 2), (- 1))) / denom)
    x = ((xg[(None, :, None)] * images).sum(axis=((- 2), (- 1))) / denom)
    return (x, y)
