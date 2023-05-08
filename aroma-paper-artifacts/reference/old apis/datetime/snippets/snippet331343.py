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


def _adgan_experiment(dataset_load_fn, dataset_name, single_class_ind, gpu_q):
    gpu_to_use = gpu_q.get()
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_to_use
    ((x_train, y_train), (x_test, y_test)) = dataset_load_fn()
    if (len(x_test) > 5000):
        chosen_inds = np.random.choice(len(x_test), 5000, replace=False)
        x_test = x_test[chosen_inds]
        y_test = y_test[chosen_inds]
    n_channels = x_train.shape[get_channels_axis()]
    input_side = x_train.shape[2]
    critic = conv_encoder(input_side, n_channels, representation_dim=1, representation_activation='linear')
    noise_size = 256
    generator = conv_decoder(input_side, n_channels=n_channels, representation_dim=noise_size)

    def prior_gen(b_size):
        return np.random.normal(size=(b_size, noise_size))
    batch_size = 128
    epochs = 100
    x_train_task = x_train[(y_train.flatten() == single_class_ind)]

    def data_gen(b_size):
        chosen_inds = np.random.choice(len(x_train_task), b_size, replace=False)
        return x_train_task[chosen_inds]
    adgan.train_wgan_with_grad_penalty(prior_gen, generator, data_gen, critic, batch_size, epochs, grad_pen_coef=20)
    scores = adgan.scores_from_adgan_generator(x_test, prior_gen, generator)
    labels = (y_test.flatten() == single_class_ind)
    res_file_name = '{}_adgan_{}_{}.npz'.format(dataset_name, get_class_name_from_index(single_class_ind, dataset_name), datetime.now().strftime('%Y-%m-%d-%H%M'))
    res_file_path = os.path.join(RESULTS_DIR, dataset_name, res_file_name)
    save_roc_pr_curve_data(scores, labels, res_file_path)
    gpu_q.put(gpu_to_use)
