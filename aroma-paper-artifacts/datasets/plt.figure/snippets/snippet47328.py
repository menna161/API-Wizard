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
    on_colour = np.array(to_rgb('xkcd:azure'))
    off_colour = np.array(to_rgb('xkcd:red'))
    for (n, (pred, gt)) in enumerate(zip(output, inp)):
        fig = plt.figure(figsize=(5, 5))
        ax = plt.gca()
        self.imshow(ax, gt)
        ax.set_axis_off()
        for (o, (top, left, height, width)) in zip(obj[n], box[n]):
            if ((not self.show_zero_boxes) and (o <= 1e-06)):
                continue
            colour = ((o * on_colour) + ((1 - o) * off_colour))
            rect = patches.Rectangle((left, top), width, height, linewidth=2, edgecolor=colour, facecolor='none')
            ax.add_patch(rect)
        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.1, hspace=0.1)
        self.savefig(('ground_truth/' + str(n)), fig, updater, is_dir=False)
