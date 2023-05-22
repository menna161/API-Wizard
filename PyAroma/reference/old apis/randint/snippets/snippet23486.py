import numpy as np
from copy import deepcopy
import time
import pickle
import pprint as pp
import torch
import torch.nn as nn
from torch.autograd import Variable
import sys, os
from AI_physicist.pytorch_net.util import to_np_array, to_Variable, filter_filename, standardize_symbolic_expression, get_coeffs, substitute
from AI_physicist.pytorch_net.net import load_model_dict
from AI_physicist.settings.global_param import PrecisionFloorLoss, COLOR_LIST, Dt
from AI_physicist.settings.filepath import theory_PATH
from sklearn.model_selection import train_test_split
import random
from AI_physicist.theory_learning.theory_model import Theory_Training
from sklearn.model_selection import train_test_split
import pandas as pd
from AI_physicist.settings.global_param import COLOR_LIST
from AI_physicist.settings.global_param import COLOR_LIST
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pylab as plt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from operator import itemgetter
import pandas as pd
import itertools
import matplotlib.pylab as plt
import matplotlib.pylab as plt
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib
import matplotlib
import matplotlib
import matplotlib
import matplotlib
import matplotlib
import matplotlib.pyplot as plt


def check_consistent(T, info_dict_single, dataset, compare_keys=['DL_pred_nets', 'DL_domain_net', 'DL_data', 'mse_with_domain', 'loss_with_domain'], threshold=[1e-06, 1e-06, 0.001, 1e-05, 0.01], verbose=False, DL_mode='DL'):
    (((X_train, y_train), (X_test, y_test), _), info) = dataset
    num = 3
    U = deepcopy(T)
    U.domain_net_on = False
    data_record = info_dict_single['data_record_1']
    num_records = len(data_record['all_losses_dict'])
    if verbose:
        print('\nfirst stage:')
    for i in range(num):
        ii = int(np.random.randint(num_records))
        U.set_net('pred_nets', load_model_dict(data_record['pred_nets_model_dict'][ii]))
        U.set_net('domain_net', load_model_dict(data_record['domain_net_model_dict'][ii]))
        U.set_loss_core('DLs', 10)
        new_losses_dict = U.get_losses(X_test, y_test, DL_mode=DL_mode)
        record_lossed_dict = data_record['all_losses_dict'][ii]
        (is_same, diff_keys) = compare_same(new_losses_dict, record_lossed_dict, compare_keys, threshold=threshold, verbose=verbose)
        if (not is_same):
            raise Exception('keys not the same: {0} duing first stage.'.format(diff_keys))
    if verbose:
        print('\nMDL1:')
    for (j, data_record) in enumerate(info_dict_single['data_record_MDL1_1']):
        num_records = len(data_record['all_losses_dict'])
        for i in range(num):
            ii = int(np.random.randint(num_records))
            U.set_net('pred_nets', load_model_dict(data_record['pred_nets_model_dict'][ii]))
            U.set_net('domain_net', load_model_dict(data_record['domain_net_model_dict'][ii]))
            U.set_loss_core('DLs', data_record['loss_precision_floor'])
            new_losses_dict = U.get_losses(X_test, y_test, DL_mode=DL_mode)
            record_lossed_dict = data_record['all_losses_dict'][ii]
            (is_same, diff_keys) = compare_same(new_losses_dict, record_lossed_dict, compare_keys, threshold=threshold, verbose=verbose)
            if (not is_same):
                raise Exception('keys not the same: {0} duing MDL1 phase {1}.'.format(diff_keys, j))
    if verbose:
        print('\nMDL2:')
    U.domain_net_on = True
    for (j, data_record) in enumerate(info_dict_single['data_record_MDL2_1']):
        num_records = len(data_record['all_losses_dict'])
        for i in range(num):
            ii = int(np.random.randint(num_records))
            U.set_net('pred_nets', load_model_dict(data_record['pred_nets_model_dict'][ii]))
            U.set_net('domain_net', load_model_dict(data_record['domain_net_model_dict'][ii]))
            U.set_loss_core('DLs', data_record['loss_precision_floor'])
            new_losses_dict = U.get_losses(X_test, y_test, DL_mode=DL_mode)
            record_lossed_dict = data_record['all_losses_dict'][ii]
            (is_same, diff_keys) = compare_same(new_losses_dict, record_lossed_dict, compare_keys, threshold=threshold, verbose=verbose)
            if (not is_same):
                raise Exception('keys not the same: {0} duing MDL2 phase {1}.'.format(diff_keys, j))
    print('Passed checking!')
