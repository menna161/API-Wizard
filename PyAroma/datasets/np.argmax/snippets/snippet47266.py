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


def _plot(self, updater, fetched):
    images = fetched['images']
    preds = fetched['preds']
    gammas = fetched['gammas']
    hard_gammas = np.argmax(gammas, axis=2)
    N = images.shape[0]
    network = updater.network
    (_, image_height, image_width, _) = images.shape
    for i in range(N):
        (fig, axes) = plt.subplots(((2 * network.k) + 2), (network.n_steps + 1), figsize=(20, 20))
        for t in range((network.n_steps + 1)):
            ax = axes[(0, t)]
            img = images[i]
            ax.imshow(img)
            if (t == 0):
                ax.set_title('ground truth')
            ax.set_xlabel('t = {}'.format(t))
            ax = axes[(1, t)]
            img = preds[(t, i, 0)]
            ax.imshow(img)
            if (t == 0):
                ax.set_title('reconstruction')
            ax.set_xlabel('t = {}'.format(t))
            for k in range(network.k):
                ax = axes[((k + 2), t)]
                img = gammas[(t, i, k, :, :, 0)]
                ax.imshow(img)
                if (t == 0):
                    ax.set_title('component {} - soft'.format(k))
                ax.set_xlabel('t = {}'.format(t))
            for k in range(network.k):
                ax = axes[(((network.k + k) + 2), t)]
                img = (hard_gammas[(t, i, :, :, 0)] == k)
                ax.imshow(img)
                if (t == 0):
                    ax.set_title('component {} - hard'.format(k))
                ax.set_xlabel('t = {}'.format(t))
        local_step = (np.inf if cfg.overwrite_plots else '{:0>10}'.format(updater.n_updates))
        path = updater.exp_dir.path_for('plots', str(i), 'stage={:0>4}_local_step={}.pdf'.format(updater.stage_idx, local_step))
        fig.savefig(path)
        plt.close(fig)
        shutil.copyfile(path, os.path.join(os.path.dirname(path), 'latest_stage{:0>4}.pdf'.format(updater.stage_idx)))
