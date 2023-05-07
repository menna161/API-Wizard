import numpy as np
import matplotlib.pyplot as plt
from hyperopt import hp, tpe, fmin
from pyodds.algo.iforest import IFOREST
from pyodds.algo.ocsvm import OCSVM
from pyodds.algo.lof import LOF
from pyodds.algo.robustcovariance import RCOV
from pyodds.algo.staticautoencoder import StaticAutoEncoder
from pyodds.algo.luminolFunc import luminolDet
from pyodds.algo.cblof import CBLOF
from pyodds.algo.knn import KNN
from pyodds.algo.hbos import HBOS
from pyodds.algo.sod import SOD
from pyodds.algo.pca import PCA
from pyodds.algo.dagmm import DAGMM
from pyodds.algo.lstmad import LSTMAD
from pyodds.algo.lstmencdec import LSTMED
from pyodds.algo.autoencoder import AUTOENCODER


def construct_search_space():
    " Search space constructed for each of the 13 baseline algorithms.\n\n    Each algorithm is set with its own parameter space, consisting of both\n    static parameters and hp.choice()\n\n    Returns\n    -------\n    space_config :  hyperopt choice containing each baseline algorithm's\n                    parameter dictionary\n        The cumulative search space for pyodds autoML.\n    "
    activation = hp.choice('activation', ['sigmoid', 'relu', 'hard_sigmoid'])
    random_state = np.random.randint(500)
    contamination = hp.choice('contamination', [0.5, 0.4, 0.3])
    space_config = hp.choice('classifier_type', [{'type': 'iforest', 'contamination': contamination, 'n_estimators': 100, 'max_samples': 'auto', 'max_features': 1.0, 'bootstrap': False, 'n_jobs': None, 'behaviour': 'old', 'random_state': random_state}, {'type': 'ocsvm', 'gamma': 'auto', 'kernel': 'rbf', 'degree': 3, 'coef0': 0.0, 'tol': 0.001, 'nu': 0.5, 'shrinking': True, 'cache_size': 200, 'verbose': False, 'max_iter': (- 1)}, {'type': 'lof', 'contamination': contamination, 'n_neighbors': 20, 'algorithm': 'auto', 'leaf_size': 30, 'metric': 'minkowski', 'p': 2, 'metric_params': None, 'novelty': True}, {'type': 'robustcovariance', 'random_state': random_state, 'store_precision': True, 'assume_centered': False, 'support_fraction': None, 'contamination': contamination}, {'type': 'staticautoencoder', 'contamination': contamination, 'epoch': 100, 'dropout_rate': 0.2, 'regularizer_weight': 0.1, 'activation': activation, 'kernel_regularizer': 0.01, 'loss_function': 'mse', 'optimizer': 'adam'}, {'type': 'cblof', 'contamination': contamination, 'n_clusters': 8, 'clustering_estimator': None, 'alpha': 0.9, 'beta': 5, 'use_weights': False, 'random_state': random_state, 'n_jobs': 1}, {'type': 'knn', 'contamination': contamination, 'n_neighbors': 5, 'method': 'largest', 'radius': 1.0, 'algorithm': 'auto', 'leaf_size': 30, 'metric': 'minkowski', 'p': 2, 'metric_params': None, 'n_jobs': 1}, {'type': 'hbos', 'contamination': contamination, 'n_bins': 10, 'alpha': 0.1, 'tol': 0.5}, {'type': 'sod', 'contamination': contamination, 'n_neighbors': 20, 'ref_set': 10, 'alpha': 0.8}, {'type': 'pca', 'contamination': contamination, 'n_components': None, 'n_selected_components': None, 'copy': True, 'whiten': False, 'svd_solver': 'auto', 'tol': 0.0, 'iterated_power': 'auto', 'random_state': random_state, 'weighted': True, 'standardization': True}, {'type': 'dagmm', 'contamination': contamination, 'num_epochs': 10, 'lambda_energy': 0.1, 'lambda_cov_diag': 0.005, 'lr': 0.001, 'batch_size': 50, 'gmm_k': 3, 'normal_percentile': 80, 'sequence_length': 30, 'autoencoder_args': None}, {'type': 'autoencoder', 'contamination': contamination, 'num_epochs': 10, 'batch_size': 20, 'lr': 0.001, 'hidden_size': 5, 'sequence_length': 30, 'train_gaussian_percentage': 0.25}, {'type': 'lstm_ad', 'contamination': contamination, 'len_in': 1, 'len_out': 10, 'num_epochs': 10, 'lr': 0.001, 'batch_size': 1}, {'type': 'lstm_ed', 'contamination': contamination, 'num_epochs': 10, 'batch_size': 20, 'lr': 0.001, 'hidden_size': 5, 'sequence_length': 30, 'train_gaussian_percentage': 0.25}])
    return space_config
