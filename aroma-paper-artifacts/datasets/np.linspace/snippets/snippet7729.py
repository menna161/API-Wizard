from __future__ import print_function
import os
import h5py
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cbook
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
from numpy import ma
from sklearn import cross_validation
from sklearn.metrics import roc_curve, auc
from itertools import cycle
from matplotlib.ticker import MaxNLocator
from copy import copy
from scipy.interpolate import interp1d


def get_weights(pt, pt_min, pt_max, pt_bins):
    (pt_hist, edges) = np.histogram(pt, bins=np.linspace(pt_min, pt_max, (pt_bins + 1)))
    pt_hist = np.true_divide(pt_hist, pt_hist.sum())
    image_weights = np.true_divide(1.0, np.take(pt_hist, (np.searchsorted(edges, pt) - 1)))
    image_weights = np.true_divide(image_weights, image_weights.mean())
    return image_weights
