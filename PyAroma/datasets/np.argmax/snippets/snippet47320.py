import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from dps import cfg
from dps.utils.tf import tf_mean_sum, RenderHook
from auto_yolo.models.core import xent_loss, normal_vae, VariationalAutoencoder


def _plot_reconstruction(self, updater, fetched):
    inp = fetched['inp']
    output = fetched['output']
    prediction = fetched.get('prediction', None)
    targets = fetched.get('targets', None)
    sqrt_N = int(np.ceil(np.sqrt(self.N)))
    fig_height = 20
    fig_width = (4.5 * fig_height)
    (fig, axes) = plt.subplots(sqrt_N, (3 * sqrt_N), figsize=(fig_width, fig_height))
    for (n, (pred, gt)) in enumerate(zip(output, inp)):
        i = int((n / sqrt_N))
        j = int((n % sqrt_N))
        ax = axes[(i, (3 * j))]
        ax.set_axis_off()
        self.imshow(ax, gt)
        if (targets is not None):
            _target = targets[n]
            _prediction = prediction[n]
            title = 'target={}, prediction={}'.format(np.argmax(_target), np.argmax(_prediction))
            ax.set_title(title)
        ax = axes[(i, ((3 * j) + 1))]
        ax.set_axis_off()
        self.imshow(ax, pred)
        ax = axes[(i, ((3 * j) + 2))]
        ax.set_axis_off()
        diff = (np.abs((gt - pred)).sum(2) / 3)
        self.imshow(ax, diff)
    plt.subplots_adjust(left=0, right=1, top=0.9, bottom=0, wspace=0.1, hspace=0.2)
    self.savefig('sampled_reconstruction', fig, updater)
