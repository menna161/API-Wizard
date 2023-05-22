import tensorflow as tf
import numpy as np
import collections
from matplotlib.colors import to_rgb
import matplotlib.pyplot as plt
from matplotlib import animation
from dps import cfg
from dps.utils import Param, square_subplots
from dps.utils.tf import build_gradient_train_op, apply_mask_and_group_at_front, build_scheduled_value, FIXED_COLLECTION
from dps.tf.updater import DataManager, Evaluator, TensorRecorder, VideoUpdater as _VideoUpdater
from dps.train import Hook


def _plot(self, updater, rollouts):
    plt.ion()
    if updater.dataset.gym_dataset.image_obs:
        obs = rollouts.obs
    else:
        obs = rollouts.image
    (fig, axes) = square_subplots(rollouts.batch_size, figsize=(5, 5))
    plt.subplots_adjust(top=0.95, bottom=0, left=0, right=1, wspace=0.1, hspace=0.1)
    images = []
    for (i, ax) in enumerate(axes.flatten()):
        ax.set_aspect('equal')
        ax.set_axis_off()
        image = ax.imshow(np.zeros(obs.shape[2:]))
        images.append(image)

    def animate(t):
        for i in range(rollouts.batch_size):
            images[i].set_array(obs[(t, i, :, :, :)])
    anim = animation.FuncAnimation(fig, animate, frames=len(rollouts), interval=500)
    path = updater.exp_dir.path_for('plots', '{}_animation.gif'.format(self.name))
    anim.save(path, writer='imagemagick')
    plt.close(fig)
