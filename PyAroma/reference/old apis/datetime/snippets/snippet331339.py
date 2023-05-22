import os
import csv
from collections import defaultdict
from glob import glob
from datetime import datetime
from multiprocessing import Manager, freeze_support, Process
import numpy as np
import scipy.stats
from scipy.special import psi, polygamma
from sklearn.metrics import roc_auc_score
from sklearn.svm import OneClassSVM
from sklearn.model_selection import ParameterGrid
from sklearn.externals.joblib import Parallel, delayed
from keras.models import Model, Input, Sequential
from keras.layers import Dense, Dropout
from keras.utils import to_categorical
from utils import load_cifar10, load_cats_vs_dogs, load_fashion_mnist, load_cifar100
from utils import save_roc_pr_curve_data, get_class_name_from_index, get_channels_axis
from transformations import Transformer
from models.wide_residual_network import create_wide_residual_network
from models.encoders_decoders import conv_encoder, conv_decoder
from models import dsebm, dagmm, adgan
import keras.backend as K


def _raw_ocsvm_experiment(dataset_load_fn, dataset_name, single_class_ind):
    ((x_train, y_train), (x_test, y_test)) = dataset_load_fn()
    x_train = x_train.reshape((len(x_train), (- 1)))
    x_test = x_test.reshape((len(x_test), (- 1)))
    x_train_task = x_train[(y_train.flatten() == single_class_ind)]
    if (dataset_name in ['cats-vs-dogs']):
        subsample_inds = np.random.choice(len(x_train_task), 5000, replace=False)
        x_train_task = x_train_task[subsample_inds]
    pg = ParameterGrid({'nu': np.linspace(0.1, 0.9, num=9), 'gamma': np.logspace((- 7), 2, num=10, base=2)})
    results = Parallel(n_jobs=6)((delayed(_train_ocsvm_and_score)(d, x_train_task, (y_test.flatten() == single_class_ind), x_test) for d in pg))
    (best_params, best_auc_score) = max(zip(pg, results), key=(lambda t: t[(- 1)]))
    best_ocsvm = OneClassSVM(**best_params).fit(x_train_task)
    scores = best_ocsvm.decision_function(x_test)
    labels = (y_test.flatten() == single_class_ind)
    res_file_name = '{}_raw-oc-svm_{}_{}.npz'.format(dataset_name, get_class_name_from_index(single_class_ind, dataset_name), datetime.now().strftime('%Y-%m-%d-%H%M'))
    res_file_path = os.path.join(RESULTS_DIR, dataset_name, res_file_name)
    save_roc_pr_curve_data(scores, labels, res_file_path)
