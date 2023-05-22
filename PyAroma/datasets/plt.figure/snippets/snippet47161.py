import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from dps import cfg
from dps.utils import Param
from dps.utils.tf import build_scheduled_value, RenderHook, tf_mean_sum
from auto_yolo.models.core import VariationalAutoencoder, normal_vae, mAP, xent_loss, concrete_binary_pre_sigmoid_sample, concrete_binary_sample_kl


def _plot_reconstruction(self, updater, fetched):
    network = updater.network
    inp = fetched['inp'].reshape(self.N, *network.obs_shape)
    scale = fetched['scale'].reshape(self.N, network.max_time_steps, 2)
    shift = fetched['shift'].reshape(self.N, network.max_time_steps, 2)
    predicted_n_digits = fetched['predicted_n_digits']
    color = 'xkcd:azure'
    for i in range(self.N):
        fig = plt.figure(figsize=(5, 5))
        ax = plt.gca()
        self.imshow(ax, inp[i])
        ax.set_axis_off()
        for t in range(predicted_n_digits[i]):
            (w, h) = scale[(i, t, :)]
            (x, y) = shift[(i, t, :)]
            transformed_x = (0.5 * (x + 1.0))
            transformed_y = (0.5 * (y + 1.0))
            height = (h * network.image_height)
            width = (w * network.image_width)
            top = ((network.image_height * transformed_y) - (height / 2))
            left = ((network.image_width * transformed_x) - (width / 2))
            rect = patches.Rectangle((left, top), width, height, linewidth=2, edgecolor=color, facecolor='none')
            ax.add_patch(rect)
        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.1, hspace=0.1)
        self.savefig(('ground_truth/' + str(i)), fig, updater, is_dir=False)
