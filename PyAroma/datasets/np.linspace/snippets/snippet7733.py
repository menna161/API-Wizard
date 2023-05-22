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


def plot_gen_dists(model, test_h5_files, labels, batch_size=32, X_datasets=None, Y_datasets=None, legend_loc=2):
    'Test model. Display signal and background distributions.\n\n    Args:\n        model: keras model to test.\n        test_h5_files: name of h5 files containing test datasets.\n        labels: labels for each dataset.\n        batch_size: integer to pass to keras.\n        X_datasets: name of X_test datasets.\n        Y_datasets: name of Y_test datasets.\n        legend_loc: int for matplotlib legend location.\n    '
    if (X_datasets is None):
        X_datasets = (['X_train'] * len(test_h5_files))
    if (Y_datasets is None):
        Y_datasets = (['Y_train'] * len(test_h5_files))
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111)
    bins = np.linspace(0, 1, 50)
    for (test_h5_file, label, X_dataset, Y_dataset) in zip(test_h5_files, labels, X_datasets, Y_datasets):
        with h5py.File(test_h5_file, 'r') as h5file:
            Y_test = h5file[Y_dataset][:]
            Y_prob = model.predict_proba(h5file[X_dataset], batch_size=batch_size, verbose=0)
            Y_prob /= Y_prob.sum(axis=1)[(:, np.newaxis)]
            sig_prob = np.array([p[0] for (p, y) in zip(Y_prob, Y_test) if (y[0] == 1)])
            ax.hist(sig_prob, bins=bins, histtype='stepfilled', normed=True, alpha=0.5, label=label)
    ax.set_xlabel('network output', fontsize=16)
    ax.set_ylabel('frequency', fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=12)
    plt.legend(fontsize=16, loc=legend_loc)
    fig.show()
