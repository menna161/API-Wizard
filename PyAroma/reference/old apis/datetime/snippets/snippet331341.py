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


def _dsebm_experiment(dataset_load_fn, dataset_name, single_class_ind, gpu_q):
    gpu_to_use = gpu_q.get()
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_to_use
    ((x_train, y_train), (x_test, y_test)) = dataset_load_fn()
    n_channels = x_train.shape[get_channels_axis()]
    input_side = x_train.shape[2]
    encoder_mdl = conv_encoder(input_side, n_channels, representation_activation='relu')
    energy_mdl = dsebm.create_energy_model(encoder_mdl)
    reconstruction_mdl = dsebm.create_reconstruction_model(energy_mdl)
    batch_size = 128
    epochs = 200
    reconstruction_mdl.compile('adam', 'mse')
    x_train_task = x_train[(y_train.flatten() == single_class_ind)]
    x_test_task = x_test[(y_test.flatten() == single_class_ind)]
    reconstruction_mdl.fit(x=x_train_task, y=x_train_task, batch_size=batch_size, epochs=epochs, validation_data=(x_test_task, x_test_task))
    scores = (- energy_mdl.predict(x_test, batch_size))
    labels = (y_test.flatten() == single_class_ind)
    res_file_name = '{}_dsebm_{}_{}.npz'.format(dataset_name, get_class_name_from_index(single_class_ind, dataset_name), datetime.now().strftime('%Y-%m-%d-%H%M'))
    res_file_path = os.path.join(RESULTS_DIR, dataset_name, res_file_name)
    save_roc_pr_curve_data(scores, labels, res_file_path)
    gpu_q.put(gpu_to_use)
