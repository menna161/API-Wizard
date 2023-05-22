from typing import List, Tuple
import tensorflow as tf
import random


def _corrupt_brightness(self, image, mask):
    '\n        Radnomly applies a random brightness change.\n        '
    cond_brightness = tf.cast(tf.random.uniform([], maxval=2, dtype=tf.int32), tf.bool)
    image = tf.cond(cond_brightness, (lambda : tf.image.random_brightness(image, 0.1)), (lambda : tf.identity(image)))
    return (image, mask)
