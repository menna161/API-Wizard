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
    (_, image_height, image_width, _) = inp.shape
    obj = fetched['obj'].reshape(self.N, (- 1))
    anchor_box = updater.network.anchor_box
    (yt, xt, ys, xs) = np.split(fetched['normalized_box'], 4, axis=(- 1))
    (yt, xt, ys, xs) = coords_to_pixel_space(yt, xt, ys, xs, (image_height, image_width), anchor_box, top_left=True)
    box = np.concatenate([yt, xt, ys, xs], axis=(- 1))
    box = box.reshape(self.N, (- 1), 4)
    pred_colour = np.array(to_rgb(self.pred_colour))
    if self.do_annotations:
        n_annotations = fetched.get('n_annotations', ([0] * self.N))
        annotations = fetched.get('annotations', None)
        gt_colour = np.array(to_rgb(self.gt_colour))
    cutoff = 0.5
    for (n, (pred, gt)) in enumerate(zip(output, inp)):
        (fig, axes) = plt.subplots(1, 3, figsize=(6, 3))
        axes = np.array(axes).reshape(3)
        ax1 = axes[0]
        self.imshow(ax1, gt)
        ax2 = axes[1]
        self.imshow(ax2, pred)
        ax3 = axes[2]
        self.imshow(ax3, pred)
        for (o, (top, left, height, width)) in zip(obj[n], box[n]):
            if (o > cutoff):
                rect = patches.Rectangle((left, top), width, height, linewidth=2, edgecolor=pred_colour, facecolor='none')
                ax3.add_patch(rect)
        if self.do_annotations:
            for k in range(n_annotations[n]):
                (valid, _, _, top, bottom, left, right) = annotations[n][k]
                if (not valid):
                    continue
                height = (bottom - top)
                width = (right - left)
                rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor=gt_colour, facecolor='none')
                ax3.add_patch(rect)
        for ax in axes.flatten():
            ax.set_axis_off()
        plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02, wspace=0.1, hspace=0.1)
        self.savefig(('sampled_reconstruction/' + str(n)), fig, updater)
