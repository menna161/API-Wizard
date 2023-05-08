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


def _transformations_experiment(dataset_load_fn, dataset_name, single_class_ind, gpu_q):
    gpu_to_use = gpu_q.get()
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_to_use
    ((x_train, y_train), (x_test, y_test)) = dataset_load_fn()
    if (dataset_name in ['cats-vs-dogs']):
        transformer = Transformer(16, 16)
        (n, k) = (16, 8)
    else:
        transformer = Transformer(8, 8)
        (n, k) = (10, 4)
    mdl = create_wide_residual_network(x_train.shape[1:], transformer.n_transforms, n, k)
    mdl.compile('adam', 'categorical_crossentropy', ['acc'])
    x_train_task = x_train[(y_train.flatten() == single_class_ind)]
    transformations_inds = np.tile(np.arange(transformer.n_transforms), len(x_train_task))
    x_train_task_transformed = transformer.transform_batch(np.repeat(x_train_task, transformer.n_transforms, axis=0), transformations_inds)
    batch_size = 128
    mdl.fit(x=x_train_task_transformed, y=to_categorical(transformations_inds), batch_size=batch_size, epochs=int(np.ceil((200 / transformer.n_transforms))))

    def calc_approx_alpha_sum(observations):
        N = len(observations)
        f = np.mean(observations, axis=0)
        return (((N * (len(f) - 1)) * (- psi(1))) / ((N * np.sum((f * np.log(f)))) - np.sum((f * np.sum(np.log(observations), axis=0)))))

    def inv_psi(y, iters=5):
        cond = (y >= (- 2.22))
        x = ((cond * (np.exp(y) + 0.5)) + (((1 - cond) * (- 1)) / (y - psi(1))))
        for _ in range(iters):
            x = (x - ((psi(x) - y) / polygamma(1, x)))
        return x

    def fixed_point_dirichlet_mle(alpha_init, log_p_hat, max_iter=1000):
        alpha_new = alpha_old = alpha_init
        for _ in range(max_iter):
            alpha_new = inv_psi((psi(np.sum(alpha_old)) + log_p_hat))
            if (np.sqrt(np.sum(((alpha_old - alpha_new) ** 2))) < 1e-09):
                break
            alpha_old = alpha_new
        return alpha_new

    def dirichlet_normality_score(alpha, p):
        return np.sum(((alpha - 1) * np.log(p)), axis=(- 1))
    scores = np.zeros((len(x_test),))
    observed_data = x_train_task
    for t_ind in range(transformer.n_transforms):
        observed_dirichlet = mdl.predict(transformer.transform_batch(observed_data, ([t_ind] * len(observed_data))), batch_size=1024)
        log_p_hat_train = np.log(observed_dirichlet).mean(axis=0)
        alpha_sum_approx = calc_approx_alpha_sum(observed_dirichlet)
        alpha_0 = (observed_dirichlet.mean(axis=0) * alpha_sum_approx)
        mle_alpha_t = fixed_point_dirichlet_mle(alpha_0, log_p_hat_train)
        x_test_p = mdl.predict(transformer.transform_batch(x_test, ([t_ind] * len(x_test))), batch_size=1024)
        scores += dirichlet_normality_score(mle_alpha_t, x_test_p)
    scores /= transformer.n_transforms
    labels = (y_test.flatten() == single_class_ind)
    res_file_name = '{}_transformations_{}_{}.npz'.format(dataset_name, get_class_name_from_index(single_class_ind, dataset_name), datetime.now().strftime('%Y-%m-%d-%H%M'))
    res_file_path = os.path.join(RESULTS_DIR, dataset_name, res_file_name)
    save_roc_pr_curve_data(scores, labels, res_file_path)
    mdl_weights_name = '{}_transformations_{}_{}_weights.h5'.format(dataset_name, get_class_name_from_index(single_class_ind, dataset_name), datetime.now().strftime('%Y-%m-%d-%H%M'))
    mdl_weights_path = os.path.join(RESULTS_DIR, dataset_name, mdl_weights_name)
    mdl.save_weights(mdl_weights_path)
    gpu_q.put(gpu_to_use)
