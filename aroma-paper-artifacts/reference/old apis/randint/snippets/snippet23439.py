import numpy as np
from sklearn.metrics import confusion_matrix
import pickle
import random
from copy import deepcopy
import datetime
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable, grad
import torch.nn.functional as F
import torch.utils.data as data_utils
from torch.optim.lr_scheduler import LambdaLR, ReduceLROnPlateau
import sys, os
from AI_physicist.theory_learning.models import Loss_Fun_Cumu, get_Lagrangian_loss
from AI_physicist.theory_learning.util_theory import forward, logplus, Loss_Decay_Scheduler, count_metrics_pytorch, plot3D, plot_indi_domain, to_one_hot, load_info_dict, get_piecewise_dataset, get_group_norm
from AI_physicist.settings.filepath import theory_PATH
from AI_physicist.settings.global_param import COLOR_LIST, PrecisionFloorLoss
from AI_physicist.pytorch_net.util import Loss_Fun, make_dir, Early_Stopping, record_data, plot_matrices, get_args, base_repr, base_repr_2_int
from AI_physicist.pytorch_net.util import sort_two_lists, to_string, Loss_with_uncertainty, get_optimizer, Gradient_Noise_Scale_Gen, to_np_array, to_Variable, to_Boolean, get_criterion
from AI_physicist.pytorch_net.net import MLP, Model_Ensemble, load_model_dict, construct_model_ensemble_from_nets, train_simple
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.pylab as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib
import matplotlib


def plot(self, X, y, forward_steps=1, view_init=(10, 190), figsize=(10, 8), show_3D_plot=False, show_vs=False, show_loss_histogram=True, is_show=True, filename=None, **kwargs):
    if (not is_show):
        import matplotlib
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    if hasattr(self, 'autoencoder'):
        X_lat = self.autoencoder.encode(X)
    else:
        X_lat = X
    (preds, valid_onehot) = get_preds_valid(self.net_dict, X, forward_steps=forward_steps, domain_net=self.domain_net, domain_pred_mode='onehot', is_Lagrangian=self.is_Lagrangian)
    best_theory_idx = get_best_model_idx(self.net_dict, X, y, loss_fun_cumu=self.loss_fun_cumu, forward_steps=forward_steps, mode='expanded', is_Lagrangian=self.is_Lagrangian)
    best_theory_onehot = to_one_hot(best_theory_idx, valid_onehot.size(1))
    true_domain = (kwargs['true_domain'] if ('true_domain' in kwargs) else None)
    if (true_domain is not None):
        uniques = np.unique(to_np_array(true_domain))
        num_uniques = int(max((np.max(uniques) + 1), len(uniques)))
        true_domain_onehot = to_one_hot(true_domain, num_uniques)
    else:
        true_domain_onehot = None
    if show_3D_plot:
        from mpl_toolkits.mplot3d import Axes3D
        loss_dict = self.get_losses(X, y, mode='all')
        if (self.input_size > 1):
            for i in range(y.size(1)):
                if is_show:
                    print('target with axis {0}:'.format(i))
                if (true_domain is not None):
                    axis_lim = plot3D(X, y[:, i:(i + 1)].repeat(1, num_uniques), true_domain_onehot, view_init=view_init, figsize=figsize, is_show=is_show, filename=((filename + '_target_ax_{0}.png'.format(i)) if (filename is not None) else None))
                else:
                    axis_lim = plot3D(X, y[:, i:(i + 1)], view_init=view_init, figsize=figsize, is_show=is_show, filename=((filename + '_target_ax_{0}.png'.format(i)) if (filename is not None) else None))
            for i in range(preds.size(2)):
                if is_show:
                    print('best_prediction with axis {0}:'.format(i))
                plot3D(X, preds[:, :, i], best_theory_onehot, view_init=view_init, axis_lim=axis_lim, axis_title=['loss_best = {0:.9f}'.format(loss_dict['loss_best']), '\n'.join(['{2}_theory_{0}: {1:.9f}'.format(j, loss_dict['loss_indi_theory'][j], self.loss_fun_cumu.loss_fun.core) for j in range(len(loss_dict['loss_indi_theory']))])], figsize=figsize, is_show=is_show, filename=((filename + '_best-prediction_ax_{0}.png'.format(i)) if (filename is not None) else None))
            for i in range(preds.size(2)):
                if is_show:
                    print('all theory prediction with axis {0}:'.format(i))
                plot3D(X, preds[:, :, i], valid_onehot, view_init=view_init, axis_lim=axis_lim, axis_title=['mse_with_domain = {0:.9f}'.format(loss_dict['mse_with_domain']), 'loss_total = {0:.9f}'.format(loss_dict['loss'])], figsize=figsize, is_show=is_show, filename=((filename + '_all-prediction_ax_{0}.png'.format(i)) if (filename is not None) else None))
        else:
            ylim = ((np.floor(preds.data.min()) - 3), (np.ceil(preds.data.max()) + 3))
            if ('uncertainty_nets' in self.net_dict):
                (pred_with_uncertainty, info_list) = get_pred_with_uncertainty(preds, self.net_dict['uncertainty_nets'], X)
                fig = plt.figure(figsize=(6, 5))
                sigma = (info_list.sum(1) ** (- 0.5))
                plt.errorbar(to_np_array(X), to_np_array(pred_with_uncertainty), yerr=to_np_array(sigma), fmt='ob', markersize=1, alpha=0.4, label='theory_whole')
                plt.ylim(ylim)
                plt.plot(to_np_array(X), to_np_array(y), '.k', markersize=2, alpha=0.9)
            else:
                for j in range(self.num_theories):
                    plt.plot(to_np_array(X), to_np_array(preds[:, j]), color=COLOR_LIST[(j % len(COLOR_LIST))], marker='.', markersize=1, alpha=0.6, label='theory_{0}'.format(j))
                plt.plot(to_np_array(X), to_np_array(y), '.k', markersize=2, alpha=0.9)
                plt.legend()
                plt.ylim(ylim)
            plt.legend()
            plt.show()
            fig = plt.figure(figsize=((self.num_theories * 6), 5))
            for j in range(self.num_theories):
                plt.subplot(1, self.num_theories, (j + 1))
                if ('uncertainty-based' in self.loss_types):
                    plt.errorbar(to_np_array(X), to_np_array(preds[:, j]), yerr=to_np_array((info_list ** (- 0.5))[:, j]), fmt='o{0}'.format(COLOR_LIST[(j % len(COLOR_LIST))]), markersize=1, alpha=0.2, label='theory_{0}'.format(j))
                else:
                    plt.plot(to_np_array(X), to_np_array(preds[:, j]), color=COLOR_LIST[(j % len(COLOR_LIST))], marker='.', markersize=1, alpha=0.6, label='theory_{0}'.format(j))
                plt.ylim(ylim)
                plt.plot(to_np_array(X), to_np_array(y), '.k', markersize=2, alpha=0.9)
                plt.legend()
            plt.show()
    if (('true_domain' in kwargs) and (kwargs['true_domain'] is not None) and ((self.input_size % 2) == 0) and (('num_output_dims' not in kwargs) or (('num_output_dims' in kwargs) and (kwargs['num_output_dims'] in [1, 2, 4]))) and (self.is_Lagrangian is not True)):
        if (('num_output_dims' in kwargs) and (kwargs['num_output_dims'] == 4)):
            idx = Variable(torch.LongTensor(np.array([0, 2])))
        else:
            idx = None
        self.get_domain_plot(X, y, X_lat=X_lat, true_domain=kwargs['true_domain'], X_idx=idx, y_idx=idx, is_plot_loss=(False if (len(y.shape) == 4) else True), is_plot_indi_domain=False, is_show=is_show, filename=((filename + '_domain-plot.png') if (filename is not None) else None), is_Lagrangian=self.is_Lagrangian)
    if show_vs:
        for i in range(preds.size(2)):
            (_, (ax1, ax2)) = plt.subplots(1, 2, sharey=True, figsize=(14, 6))
            self.plot_pred_vs_y(preds[:, :, i], y[:, i:(i + 1)], best_theory_onehot, title='best_prediction_ax_{0}'.format(i), ax=ax1, is_color=True, is_show=False, filename=((filename + '_pred-vs-target_ax_{0}.png'.format(i)) if (filename is not None) else None), is_close=False)
            self.plot_pred_vs_y(preds[:, :, i], y[:, i:(i + 1)], valid_onehot, title='domain_prediction_ax_{0}'.format(i), ax=ax2, is_color=True, is_show=is_show, filename=((filename + '_pred-vs-target_ax_{0}.png'.format(i)) if (filename is not None) else None))
    if (is_show and hasattr(self, 'autoencoder')):
        loss_indi_theory = []
        for k in range(self.num_theories):
            loss_indi_theory.append(to_np_array(self.loss_fun_cumu(preds[:, k:(k + 1)], y, is_mean=False)))
        loss_indi_theory = np.concatenate(loss_indi_theory, 1)
        domains = to_np_array(self.domain_net(X_lat).max(1)[1])
        X_recons = self.autoencoder(X)
        print('reconstruct:')
        for i in np.random.randint(len(X), size=2):
            plot_matrices(torch.cat([X[i], X_recons[i]], 0), images_per_row=5)
        print('prediction:')
        for i in np.random.randint(len(X), size=10):
            print('losses: {0}'.format(to_string(loss_indi_theory[i], connect='\t', num_digits=6)))
            print('best_idx: {0}\tdomain_idx: {1}'.format(to_np_array(best_theory_idx[i]), domains[i]))
            plot_matrices(torch.cat([y[i], preds[i]], 0), images_per_row=5)
    if show_loss_histogram:
        self.plot_loss_histogram(X, y, X_lat=X_lat, mode='log-mse', forward_steps=forward_steps, is_show=is_show, filename=filename)
        self.plot_loss_histogram(X, y, X_lat=X_lat, mode=('DL' if (not (('DL' in self.loss_core) and (self.loss_core != 'DL'))) else self.loss_core), forward_steps=forward_steps, is_show=is_show, filename=filename)
    plt.clf()
    plt.close()
