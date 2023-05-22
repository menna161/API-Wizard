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


def prepare_datasets(sig_h5_file, bkd_h5_file, dataset_name='dataset', n_sig=(- 1), n_bkd=(- 1), test_frac=0.1, val_frac=0.0, n_folds=1, shuffle=True, shuffle_seed=1, balance=True):
    'Prepare datasets for network training.\n\n    Combine signal and background images; k-fold into training, validation,\n    test sets. Save to files.\n\n    Args:\n        sig_h5_file, bkd_h5_file: location of h5 files containing signal,\n                                  background images.\n        dataset_name: base filename to use for saving datasets.\n        n_sig, n_bkd: number of signal, background images to load.\n        test_frac: proportion of images to save for testing.\n        val_frac: proportion of images to save for validation. Leave at zero\n                  unless using ROC AUC scoring.\n        n_folds: number of k-folds.\n        auxvars: list of auxvar field names to load.\n        shuffle: if True shuffle images before k-folding.\n        shuffle_seed: seed for shuffling.\n    Returns:\n        file_dict: dict containing list of filenames containing train, test\n                   datasets.\n    TODO: add support for multiple classes.\n    '
    (sig_images, sig_auxvars) = load_images(sig_h5_file, n_sig)
    (bkd_images, bkd_auxvars) = load_images(bkd_h5_file, n_bkd)
    if balance:
        n = min(len(sig_images), len(bkd_images))
        sig_images = sig_images[:n]
        sig_auxvars = sig_auxvars[:n]
        bkd_images = bkd_images[:n]
        bkd_auxvars = bkd_auxvars[:n]
    n_sig = len(sig_images)
    n_bkd = len(bkd_images)
    print('collected {0} signal and {1} background images'.format(n_sig, n_bkd))
    n_images = (n_sig + n_bkd)
    images = np.concatenate((sig_images, bkd_images))
    images = images.reshape((- 1), (images.shape[1] * images.shape[2]))
    auxvars = np.concatenate((sig_auxvars, bkd_auxvars))
    classes = np.concatenate([np.repeat([[1, 0]], n_sig, axis=0), np.repeat([[0, 1]], n_bkd, axis=0)])
    if (test_frac >= 1):
        out_file = (dataset_name + '_test.h5')
        with h5py.File(out_file, 'w') as h5file:
            h5file.create_dataset('X_test', data=images)
            h5file.create_dataset('Y_test', data=classes)
            h5file.create_dataset('auxvars_test', data=auxvars)
        return {'test': out_file}
    if (test_frac <= 0):
        rs = np.random.RandomState(shuffle_seed)
        train = np.arange(len(images))
        rs.shuffle(train)
        out_file = (dataset_name + '_train.h5')
        with h5py.File(out_file, 'w') as h5file:
            n_val = int((val_frac * len(train)))
            h5file.create_dataset('X_val', data=images[train][:n_val])
            h5file.create_dataset('Y_val', data=classes[train][:n_val])
            h5file.create_dataset('auxvars_val', data=auxvars[train][:n_val])
            h5file.create_dataset('X_train', data=images[train][n_val:])
            h5file.create_dataset('Y_train', data=classes[train][n_val:])
            h5file.create_dataset('auxvars_train', data=auxvars[train][n_val:])
        return {'train': out_file}
    rs = cross_validation.ShuffleSplit(n_images, n_iter=1, test_size=test_frac, random_state=shuffle_seed)
    for (trn, tst) in rs:
        (train, test) = (trn, tst)
    out_file = (dataset_name + '_test.h5')
    with h5py.File(out_file, 'w') as h5file:
        h5file.create_dataset('X_test', data=images[test])
        h5file.create_dataset('Y_test', data=classes[test])
        h5file.create_dataset('auxvars_test', data=auxvars[test])
    file_dict = {'test': out_file}
    if (n_folds > 1):
        kf = cross_validation.KFold(len(train), n_folds, shuffle=True, random_state=shuffle_seed)
        i = 0
        kf_files = []
        for (ktrain, ktest) in kf:
            np.random.shuffle(ktrain)
            out_file = (dataset_name + '_train_kf{0}.h5'.format(i))
            with h5py.File(out_file, 'w') as h5file:
                h5file.create_dataset('X_test', data=images[train][ktest])
                h5file.create_dataset('Y_test', data=classes[train][ktest])
                h5file.create_dataset('auxvars_test', data=auxvars[train][ktest])
                n_val = int((val_frac * len(ktrain)))
                h5file.create_dataset('X_val', data=images[train][ktrain][:n_val])
                h5file.create_dataset('Y_val', data=classes[train][ktrain][:n_val])
                h5file.create_dataset('auxvars_val', data=auxvars[train][ktrain][:n_val])
                h5file.create_dataset('X_train', data=images[train][ktrain][n_val:])
                h5file.create_dataset('Y_train', data=classes[train][ktrain][n_val:])
                h5file.create_dataset('auxvars_train', data=auxvars[train][ktrain][n_val:])
            kf_files.append(out_file)
            i += 1
        file_dict['train'] = kf_files
    else:
        rs = np.random.RandomState(shuffle_seed)
        rs.shuffle(train)
        out_file = (dataset_name + '_train.h5')
        with h5py.File(out_file, 'w') as h5file:
            n_val = int((val_frac * len(train)))
            h5file.create_dataset('X_val', data=images[train][:n_val])
            h5file.create_dataset('Y_val', data=classes[train][:n_val])
            h5file.create_dataset('auxvars_val', data=auxvars[train][:n_val])
            h5file.create_dataset('X_train', data=images[train][n_val:])
            h5file.create_dataset('Y_train', data=classes[train][n_val:])
            h5file.create_dataset('auxvars_train', data=auxvars[train][n_val:])
        file_dict['train'] = out_file
    return file_dict
