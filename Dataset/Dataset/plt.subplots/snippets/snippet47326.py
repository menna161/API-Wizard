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


def _plot_patches(self, updater, fetched, N):
    import matplotlib.pyplot as plt
    (H, W, B) = (updater.network.H, updater.network.W, updater.network.B)
    glimpse = fetched.get('glimpse', None)
    appearance = fetched['appearance']
    obj = fetched['obj']
    z = fetched['z']
    on_colour = np.array(to_rgb('xkcd:azure'))
    off_colour = np.array(to_rgb('xkcd:red'))
    for idx in range(N):
        (fig, axes) = plt.subplots((3 * H), (W * B), figsize=(20, 20))
        axes = np.array(axes).reshape((3 * H), (W * B))
        cell_idx = 0
        for (h, w, b) in itertools.product(range(H), range(W), range(B)):
            _obj = obj[(idx, cell_idx, 0)]
            _z = z[(idx, cell_idx, 0)]
            ax = axes[((3 * h), ((w * B) + b))]
            self.imshow(ax, appearance[(idx, cell_idx, :, :, :3)])
            colour = ((_obj * on_colour) + ((1 - _obj) * off_colour))
            obj_rect = patches.Rectangle((1, 0), 0.2, 1, clip_on=False, transform=ax.transAxes, facecolor=colour)
            ax.add_patch(obj_rect)
            if ((h == 0) and (b == 0)):
                ax.set_title('w={}'.format(w))
            if ((w == 0) and (b == 0)):
                ax.set_ylabel('h={}'.format(h))
            ax = axes[(((3 * h) + 1), ((w * B) + b))]
            self.imshow(ax, appearance[(idx, cell_idx, :, :, 3)], cmap='gray')
            ax.set_title('obj={:.2f}, z={:.2f}, b={}'.format(_obj, _z, b))
            ax = axes[(((3 * h) + 2), ((w * B) + b))]
            ax.set_title('input glimpse')
            self.imshow(ax, glimpse[(idx, cell_idx, :, :, :)])
            cell_idx += 1
        for ax in axes.flatten():
            ax.set_axis_off()
        plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02, wspace=0.1, hspace=0.1)
        self.savefig(('sampled_patches/' + str(idx)), fig, updater)
