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

if (__name__ == '__main__'):
    from contextlib import ExitStack
    with NumpySeed(100000):
        (sprites, scales, offsets, backgrounds) = _get_data()
        device = 'gpu'
        print('Running...')
        session_config = tf.ConfigProto()
        session_config.log_device_placement = 1
        session_config.gpu_options.per_process_gpu_memory_fraction = 0.1
        session_config.gpu_options.allow_growth = True
        graph = tf.Graph()
        sess = tf.Session(graph=graph, config=session_config)
        with ExitStack() as stack:
            stack.enter_context(graph.as_default())
            stack.enter_context(sess)
            stack.enter_context(sess.as_default())
            sprites_ph = [tf.placeholder(tf.float32, (None, *s.shape[1:])) for s in sprites]
            scales_ph = [tf.placeholder(tf.float32, (None, *s.shape[1:])) for s in scales]
            offsets_ph = [tf.placeholder(tf.float32, (None, *s.shape[1:])) for s in offsets]
            backgrounds_ph = tf.placeholder(tf.float32, (None, *backgrounds.shape[1:]))
            with tf.device('/{}:0'.format(device)):
                images = render_sprites.render_sprites(sprites_ph, scales_ph, offsets_ph, backgrounds_ph)
            d = {}
            d.update({ph: a for (ph, a) in zip(sprites_ph, sprites)})
            d.update({ph: a for (ph, a) in zip(scales_ph, scales)})
            d.update({ph: a for (ph, a) in zip(offsets_ph, offsets)})
            d[backgrounds_ph] = backgrounds
            result = sess.run(images, feed_dict=d)
        from dps.utils import image_to_string
        print(image_to_string(result[(0, ..., 0)]))
        print()
        print(image_to_string(result[(0, ..., 1)]))
        print()
        print(image_to_string(result[(0, ..., 2)]))
        print()
        print(result)
        print('Done running.')
        result = np.clip(result, 1e-06, (1 - 1e-06))
        import matplotlib.pyplot as plt
        from dps.utils import square_subplots
        (fig, axes) = square_subplots(len(sprites[0]))
        fig.suptitle(device)
        for (img, ax) in zip(result, axes.flatten()):
            ax.imshow(img)
        plt.show()
