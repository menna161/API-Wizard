from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from dreamer.tools import count_dataset
from dreamer.tools import gif_summary
from dreamer.tools import image_strip_summary
from dreamer.tools import shape as shapelib


def image_summaries(dist, target, name='image', max_batch=6):
    summaries = []
    with tf.variable_scope(name):
        image = dist.mode()[:max_batch]
        target = target[:max_batch]
        error = (((image - target) + 1) / 2)
        summaries.append(image_strip_summary.image_strip_summary('prediction', image))
        frames = tf.concat([target, image, error], 2)
        frames = tf.transpose(frames, [1, 2, 0, 3, 4])
        s = shapelib.shape(frames)
        frames = tf.reshape(frames, [s[0], s[1], (s[2] * s[3]), s[4]])
        summaries.append(gif_summary.gif_summary('gif', frames[None], max_outputs=1, fps=20))
    return summaries
