from typing import List, Tuple
import tensorflow as tf
import random


def _corrupt_contrast(self, image, mask):
    '\n        Randomly applies a random contrast change.\n        '
    cond_contrast = tf.cast(tf.random.uniform([], maxval=2, dtype=tf.int32), tf.bool)
    image = tf.cond(cond_contrast, (lambda : tf.image.random_contrast(image, 0.1, 0.8)), (lambda : tf.identity(image)))
    return (image, mask)
