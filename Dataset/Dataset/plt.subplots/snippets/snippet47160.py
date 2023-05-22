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
    output = fetched['output'].reshape(self.N, *network.obs_shape)
    object_shape = network.object_shape
    vae_input = fetched['vae_input'].reshape(self.N, network.max_time_steps, *object_shape, network.image_depth)
    vae_output = fetched['vae_output'].reshape(self.N, network.max_time_steps, *object_shape, network.image_depth)
    scale = fetched['scale'].reshape(self.N, network.max_time_steps, 2)
    shift = fetched['shift'].reshape(self.N, network.max_time_steps, 2)
    predicted_n_digits = fetched['predicted_n_digits']
    annotations = fetched['annotations']
    n_annotations = fetched['n_annotations']
    color_order = plt.rcParams['axes.prop_cycle'].by_key()['color']
    max_n_digits = max(predicted_n_digits)
    fig_width = 30
    (fig, axes) = plt.subplots((max_n_digits + 1), (2 * self.N), figsize=(fig_width, (((max_n_digits + 1) / (2 * self.N)) * fig_width)))
    for i in range(self.N):
        ax_gt = axes[(0, (2 * i))]
        self.imshow(ax_gt, inp[i])
        ax_gt.set_axis_off()
        ax_rec = axes[(0, ((2 * i) + 1))]
        self.imshow(ax_rec, output[i])
        ax_rec.set_axis_off()
        for j in range(n_annotations[i]):
            (valid, _, _, t, b, l, r) = annotations[i][j]
            if (not valid):
                continue
            h = (b - t)
            w = (r - l)
            rect = patches.Rectangle((l, t), w, h, linewidth=1, edgecolor='white', facecolor='none')
            ax_gt.add_patch(rect)
            rect = patches.Rectangle((l, t), w, h, linewidth=1, edgecolor='white', facecolor='none')
            ax_rec.add_patch(rect)
        for t in range(max_n_digits):
            axes[((t + 1), (2 * i))].set_axis_off()
            axes[((t + 1), ((2 * i) + 1))].set_axis_off()
            if (t >= predicted_n_digits[i]):
                axes[((t + 1), (2 * i))].set_aspect('equal')
                axes[((t + 1), ((2 * i) + 1))].set_aspect('equal')
                continue
            (w, h) = scale[(i, t, :)]
            (x, y) = shift[(i, t, :)]
            transformed_x = (0.5 * (x + 1.0))
            transformed_y = (0.5 * (y + 1.0))
            height = (h * network.image_height)
            width = (w * network.image_width)
            top = ((network.image_height * transformed_y) - (height / 2))
            left = ((network.image_width * transformed_x) - (width / 2))
            rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor=color_order[t], facecolor='none')
            ax_rec.add_patch(rect)
            rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor=color_order[t], facecolor='none')
            ax_gt.add_patch(rect)
            ax = axes[((t + 1), (2 * i))]
            self.imshow(ax, vae_input[(i, t)])
            ax.set_ylabel('t={}'.format(t))
            obj_rect = patches.Rectangle((1, 0), 0.2, 1, clip_on=False, transform=ax.transAxes, facecolor=color_order[t])
            ax.add_patch(obj_rect)
            ax = axes[((t + 1), ((2 * i) + 1))]
            self.imshow(ax, vae_output[(i, t)])
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.14, hspace=0.1)
    self.savefig('sampled_reconstruction', fig, updater)
