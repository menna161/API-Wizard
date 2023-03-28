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


def _dagmm_experiment(dataset_load_fn, dataset_name, single_class_ind, gpu_q):
    gpu_to_use = gpu_q.get()
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_to_use
    ((x_train, y_train), (x_test, y_test)) = dataset_load_fn()
    n_channels = x_train.shape[get_channels_axis()]
    input_side = x_train.shape[2]
    enc = conv_encoder(input_side, n_channels, representation_dim=5, representation_activation='linear')
    dec = conv_decoder(input_side, n_channels=n_channels, representation_dim=enc.output_shape[(- 1)])
    n_components = 3
    estimation = Sequential([Dense(64, activation='tanh', input_dim=(enc.output_shape[(- 1)] + 2)), Dropout(0.5), Dense(10, activation='tanh'), Dropout(0.5), Dense(n_components, activation='softmax')])
    batch_size = 256
    epochs = 200
    lambda_diag = 0.0005
    lambda_energy = 0.01
    dagmm_mdl = dagmm.create_dagmm_model(enc, dec, estimation, lambda_diag)
    dagmm_mdl.compile('adam', ['mse', (lambda y_true, y_pred: (lambda_energy * y_pred))])
    x_train_task = x_train[(y_train.flatten() == single_class_ind)]
    x_test_task = x_test[(y_test.flatten() == single_class_ind)]
    dagmm_mdl.fit(x=x_train_task, y=[x_train_task, np.zeros((len(x_train_task), 1))], batch_size=batch_size, epochs=epochs, validation_data=(x_test_task, [x_test_task, np.zeros((len(x_test_task), 1))]))
    energy_mdl = Model(dagmm_mdl.input, dagmm_mdl.output[(- 1)])
    scores = (- energy_mdl.predict(x_test, batch_size))
    scores = scores.flatten()
    if (not np.all(np.isfinite(scores))):
        min_finite = np.min(scores[np.isfinite(scores)])
        scores[(~ np.isfinite(scores))] = (min_finite - 1)
    labels = (y_test.flatten() == single_class_ind)
    res_file_name = '{}_dagmm_{}_{}.npz'.format(dataset_name, get_class_name_from_index(single_class_ind, dataset_name), datetime.now().strftime('%Y-%m-%d-%H%M'))
    res_file_path = os.path.join(RESULTS_DIR, dataset_name, res_file_name)
    save_roc_pr_curve_data(scores, labels, res_file_path)
    gpu_q.put(gpu_to_use)
