from typing import List, Tuple
import tensorflow as tf
import random


def _corrupt_saturation(self, image, mask):
    '\n        Randomly applies a random saturation change.\n        '
    cond_saturation = tf.cast(tf.random.uniform([], maxval=2, dtype=tf.int32), tf.bool)
    image = tf.cond(cond_saturation, (lambda : tf.image.random_saturation(image, 0.1, 0.8)), (lambda : tf.identity(image)))
    return (image, mask)
