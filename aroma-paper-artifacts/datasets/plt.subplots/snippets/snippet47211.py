from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import tensorflow.contrib.slim as slim
from tensorflow.contrib import distributions as dist
from tensorflow.contrib.rnn import RNNCell
import numpy as np
from matplotlib.colors import hsv_to_rgb
import matplotlib.pyplot as plt
import os
import shutil
from dps import cfg
from dps.utils import Param
from dps.utils.tf import ScopedFunction


def overview_plot(i, gammas, preds, inputs, corrupted=None, **kwargs):
    (T, B, K, H, W, C) = gammas.shape
    T -= 1
    corrupted = (corrupted if (corrupted is not None) else inputs)
    gamma_colors = get_gamma_colors(K)
    inputs = inputs[(:, i, 0)]
    gammas = gammas[(:, i, :, :, :, 0)]
    if (preds.shape[1] != B):
        preds = preds[(:, 0)]
    preds = preds[(:, i)]
    corrupted = corrupted[(:, i, 0)]
    inputs = np.clip(inputs, 0.0, 1.0)
    preds = np.clip(preds, 0.0, 1.0)
    corrupted = np.clip(corrupted, 0.0, 1.0)

    def plot_img(ax, data, cmap='Greys_r', xlabel=None, ylabel=None, border_color=None):
        if (data.shape[(- 1)] == 1):
            ax.matshow(data[(:, :, 0)], cmap=cmap, vmin=0.0, vmax=1.0, interpolation='nearest')
        else:
            ax.imshow(data, interpolation='nearest')
        ax.set_xticks([])
        ax.set_yticks([])
        (ax.set_xlabel(xlabel, color=(border_color or 'k')) if xlabel else None)
        (ax.set_ylabel(ylabel, color=(border_color or 'k')) if ylabel else None)
        if border_color:
            color_spines(ax, color=border_color)

    def plot_gamma(ax, gamma, xlabel=None, ylabel=None):
        gamma = np.transpose(gamma, [1, 2, 0])
        gamma = gamma.reshape((- 1), gamma.shape[(- 1)]).dot(gamma_colors).reshape((gamma.shape[:(- 1)] + (3,)))
        ax.imshow(gamma, interpolation='nearest')
        ax.set_xticks([])
        ax.set_yticks([])
        (ax.set_xlabel(xlabel) if xlabel else None)
        (ax.set_ylabel(ylabel) if ylabel else None)
    (nrows, ncols) = ((K + 4), (T + 1))
    (fig, axes) = plt.subplots(nrows=nrows, ncols=ncols, figsize=((2 * ncols), (2 * nrows)))
    axes[(0, 0)].set_visible(False)
    axes[(1, 0)].set_visible(False)
    plot_gamma(axes[(2, 0)], gammas[0], ylabel='Gammas')
    for k in range((K + 1)):
        axes[((k + 3), 0)].set_visible(False)
    for t in range(1, (T + 1)):
        g = gammas[t]
        p = preds[t]
        reconst = np.sum((g[(:, :, :, None)] * p), axis=0)
        plot_img(axes[(0, t)], inputs[t])
        plot_img(axes[(1, t)], reconst)
        plot_gamma(axes[(2, t)], g)
        for k in range(K):
            plot_img(axes[((k + 3), t)], p[k], border_color=tuple(gamma_colors[k]), ylabel=('mu_{}'.format(k) if (t == 1) else None))
        plot_img(axes[((K + 3), t)], corrupted[(t - 1)])
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig
