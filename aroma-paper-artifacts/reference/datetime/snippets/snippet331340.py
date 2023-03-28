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


def _cae_ocsvm_experiment(dataset_load_fn, dataset_name, single_class_ind, gpu_q):
    gpu_to_use = gpu_q.get()
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_to_use
    ((x_train, y_train), (x_test, y_test)) = dataset_load_fn()
    n_channels = x_train.shape[get_channels_axis()]
    input_side = x_train.shape[2]
    enc = conv_encoder(input_side, n_channels)
    dec = conv_decoder(input_side, n_channels)
    x_in = Input(shape=x_train.shape[1:])
    x_rec = dec(enc(x_in))
    cae = Model(x_in, x_rec)
    cae.compile('adam', 'mse')
    x_train_task = x_train[(y_train.flatten() == single_class_ind)]
    x_test_task = x_test[(y_test.flatten() == single_class_ind)]
    cae.fit(x=x_train_task, y=x_train_task, batch_size=128, epochs=200, validation_data=(x_test_task, x_test_task))
    x_train_task_rep = enc.predict(x_train_task, batch_size=128)
    if (dataset_name in ['cats-vs-dogs']):
        subsample_inds = np.random.choice(len(x_train_task_rep), 2500, replace=False)
        x_train_task_rep = x_train_task_rep[subsample_inds]
    x_test_rep = enc.predict(x_test, batch_size=128)
    pg = ParameterGrid({'nu': np.linspace(0.1, 0.9, num=9), 'gamma': np.logspace((- 7), 2, num=10, base=2)})
    results = Parallel(n_jobs=6)((delayed(_train_ocsvm_and_score)(d, x_train_task_rep, (y_test.flatten() == single_class_ind), x_test_rep) for d in pg))
    (best_params, best_auc_score) = max(zip(pg, results), key=(lambda t: t[(- 1)]))
    print(best_params)
    best_ocsvm = OneClassSVM(**best_params).fit(x_train_task_rep)
    scores = best_ocsvm.decision_function(x_test_rep)
    labels = (y_test.flatten() == single_class_ind)
    res_file_name = '{}_cae-oc-svm_{}_{}.npz'.format(dataset_name, get_class_name_from_index(single_class_ind, dataset_name), datetime.now().strftime('%Y-%m-%d-%H%M'))
    res_file_path = os.path.join(RESULTS_DIR, dataset_name, res_file_name)
    save_roc_pr_curve_data(scores, labels, res_file_path)
    gpu_q.put(gpu_to_use)
