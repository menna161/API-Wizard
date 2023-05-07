import tensorflow as tf
from tensorflow.python.framework import constant_op
from tensorflow.python.ops import gradient_checker
import numpy as np
import pytest
import os
import imageio
import matplotlib as mpl
import dps
from dps.datasets.load import load_backgrounds
from dps.datasets.base import EmnistDataset
from dps.utils import NumpySeed, resize_image
from auto_yolo.tf_ops import render_sprites
from contextlib import ExitStack
import matplotlib.pyplot as plt
from dps.utils import image_to_string
import matplotlib.pyplot as plt
from dps.utils import square_subplots


def run(device, show_plots, process_data=None, **get_data_kwargs):
    with NumpySeed(100):
        data = get_data(**get_data_kwargs)
        if (process_data is None):
            process_data = (lambda *x: x)
        (sprites, scales, offsets, backgrounds) = process_data(*data)
        with tf.device('/{}:0'.format(device)):
            images = render_sprites.render_sprites(sprites, scales, offsets, backgrounds)
            sess = get_session()
            result = sess.run(images)
        result = np.clip(result, 1e-06, (1 - 1e-06))
    if show_plots:
        import matplotlib.pyplot as plt
        (fig, (ax1, ax2)) = plt.subplots(1, 2)
        ax1.imshow(result[0])
        ax2.imshow(result[1])
        plt.show()
