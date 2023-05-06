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


def plot_sig_bkd_dists(model, test_h5_file, batch_size=32, X_dataset='X_test', Y_dataset='Y_test', legend_loc=2):
    'Test model. Display signal and background distributions.\n\n    Args:\n        model: keras model to test.\n        test_h5_file: name of h5 file containing test datasets.\n        batch_size: integer to pass to keras.\n        X_dataset: name of X_test dataset.\n        Y_dataset: name of Y_test dataset.\n        legend_loc: int for matplotlib legend location.\n    '
    with h5py.File(test_h5_file, 'r') as h5file:
        Y_test = h5file[Y_dataset][:]
        Y_prob = model.predict_proba(h5file[X_dataset], batch_size=batch_size, verbose=0)
    Y_prob /= Y_prob.sum(axis=1)[(:, np.newaxis)]
    sig_prob = np.array([p[0] for (p, y) in zip(Y_prob, Y_test) if (y[0] == 1)])
    bkd_prob = np.array([p[0] for (p, y) in zip(Y_prob, Y_test) if (y[0] == 0)])
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111)
    bins = np.linspace(0, 1, 50)
    ax.hist(sig_prob, bins=bins, histtype='stepfilled', normed=True, color='b', alpha=0.5, label='signal')
    ax.hist(bkd_prob, bins=bins, histtype='stepfilled', normed=True, color='r', alpha=0.5, label='background')
    ax.set_xlabel('network output', fontsize=16)
    ax.set_ylabel('frequency', fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=12)
    plt.legend(fontsize=16, loc=legend_loc)
    fig.show()
