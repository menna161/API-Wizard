import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import to_rgb
import itertools
from dps.utils import Param
from dps.utils.tf import tf_mean_sum, RenderHook, GridConvNet
from auto_yolo.models.core import AP, xent_loss, VariationalAutoencoder, coords_to_pixel_space
from auto_yolo.models.object_layer import ConvGridObjectLayer, GridObjectLayer, ObjectRenderer
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


def _plot_reconstruction(self, updater, fetched):
    inp = fetched['inp']
    output = fetched['output']
    prediction = fetched.get('prediction', None)
    targets = fetched.get('targets', None)
    (_, image_height, image_width, _) = inp.shape
    obj = fetched['obj'].reshape(self.N, (- 1))
    anchor_box = updater.network.anchor_box
    (yt, xt, ys, xs) = np.split(fetched['normalized_box'], 4, axis=(- 1))
    (yt, xt, ys, xs) = coords_to_pixel_space(yt, xt, ys, xs, (image_height, image_width), anchor_box, top_left=True)
    box = np.concatenate([yt, xt, ys, xs], axis=(- 1))
    box = box.reshape(self.N, (- 1), 4)
    n_annotations = fetched.get('n_annotations', ([0] * self.N))
    annotations = fetched.get('annotations', None)
    actions = fetched.get('actions', None)
    sqrt_N = int(np.ceil(np.sqrt(self.N)))
    on_colour = np.array(to_rgb('xkcd:azure'))
    off_colour = np.array(to_rgb('xkcd:red'))
    cutoff = 0.5
    (fig, axes) = plt.subplots((2 * sqrt_N), (2 * sqrt_N), figsize=(20, 20))
    axes = np.array(axes).reshape((2 * sqrt_N), (2 * sqrt_N))
    for (n, (pred, gt)) in enumerate(zip(output, inp)):
        i = int((n / sqrt_N))
        j = int((n % sqrt_N))
        ax1 = axes[((2 * i), (2 * j))]
        self.imshow(ax1, gt)
        title = ''
        if (prediction is not None):
            title += 'target={}, prediction={}'.format(np.argmax(targets[n]), np.argmax(prediction[n]))
        if (actions is not None):
            title += ', actions={}'.format(actions[(n, 0)])
        ax1.set_title(title)
        ax2 = axes[((2 * i), ((2 * j) + 1))]
        self.imshow(ax2, pred)
        ax3 = axes[(((2 * i) + 1), (2 * j))]
        self.imshow(ax3, pred)
        ax4 = axes[(((2 * i) + 1), ((2 * j) + 1))]
        self.imshow(ax4, pred)
        for (o, (top, left, height, width)) in zip(obj[n], box[n]):
            colour = ((o * on_colour) + ((1 - o) * off_colour))
            rect = patches.Rectangle((left, top), width, height, linewidth=2, edgecolor=colour, facecolor='none')
            ax4.add_patch(rect)
            if (o > cutoff):
                rect = patches.Rectangle((left, top), width, height, linewidth=2, edgecolor=colour, facecolor='none')
                ax3.add_patch(rect)
        for k in range(n_annotations[n]):
            (valid, _, _, top, bottom, left, right) = annotations[n][k]
            if (not valid):
                continue
            height = (bottom - top)
            width = (right - left)
            rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor='xkcd:yellow', facecolor='none')
            ax1.add_patch(rect)
            rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor='xkcd:yellow', facecolor='none')
            ax3.add_patch(rect)
            rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor='xkcd:yellow', facecolor='none')
            ax4.add_patch(rect)
        for ax in axes.flatten():
            ax.set_axis_off()
    if (prediction is None):
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0.1, hspace=0.1)
    else:
        plt.subplots_adjust(left=0, right=1, top=0.9, bottom=0, wspace=0.1, hspace=0.2)
    self.savefig('sampled_reconstruction', fig, updater)
