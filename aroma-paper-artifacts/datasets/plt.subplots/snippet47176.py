import tensorflow as tf
from tensorflow.python.ops.rnn import dynamic_rnn
import numpy as np
import sonnet as snt
from matplotlib.colors import to_rgb
import matplotlib.patches as patches
import shutil
import os
from dps import cfg
from dps.utils import Param
from dps.utils.tf import RNNCell, tf_mean_sum, tf_shape, tf_cosine_similarity
from auto_yolo.tf_ops import render_sprites
from auto_yolo.models import yolo_air
from auto_yolo.models.core import xent_loss, AP, VariationalAutoencoder, normal_vae
import matplotlib.pyplot as plt


def _plot_patches(self, updater, fetched, N):
    import matplotlib.pyplot as plt
    glimpse = fetched.get('glimpse', None)
    objects = fetched['objects']
    obj = fetched['obj']
    n_objects = obj.sum(axis=(1, 2)).astype('i')
    on_colour = np.array(to_rgb('xkcd:azure'))
    off_colour = np.array(to_rgb('xkcd:red'))
    for idx in range(N):
        no = n_objects[idx]
        (fig, axes) = plt.subplots(2, no, figsize=(20, 20))
        axes = np.array(axes).reshape(2, no)
        for i in range(no):
            _obj = obj[(idx, i, 0)]
            ax = axes[(0, i)]
            ax.imshow(objects[(idx, i, :, :, :)], vmin=0.0, vmax=1.0)
            colour = ((_obj * on_colour) + ((1 - _obj) * off_colour))
            obj_rect = patches.Rectangle((1, 0), 0.2, 1, clip_on=False, transform=ax.transAxes, facecolor=colour)
            ax.add_patch(obj_rect)
            ax = axes[(1, i)]
            ax.set_title('input glimpse')
            ax.imshow(glimpse[(idx, i, :, :, :)], vmin=0.0, vmax=1.0)
        plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02, wspace=0.1, hspace=0.1)
        local_step = (np.inf if cfg.overwrite_plots else '{:0>10}'.format(updater.n_updates))
        path = updater.exp_dir.path_for('plots', 'sampled_patches', str(idx), 'stage={:0>4}_local_step={}.pdf'.format(updater.stage_idx, local_step))
        fig.savefig(path)
        plt.close(fig)
        shutil.copyfile(path, os.path.join(os.path.dirname(path), 'latest_stage{:0>4}.pdf'.format(updater.stage_idx)))
