from typing import List, Tuple
import tensorflow as tf
import random


def _flip_left_right(self, image, mask):
    '\n        Randomly flips image and mask left or right in accord.\n        '
    comb_tensor = tf.concat([image, mask], axis=2)
    comb_tensor = tf.image.random_flip_left_right(comb_tensor, seed=self.seed)
    (image, mask) = tf.split(comb_tensor, [self.channels[0], self.channels[1]], axis=2)
    return (image, mask)
