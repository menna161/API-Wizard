from typing import List, Tuple
import tensorflow as tf
import random


def _crop_random(self, image, mask):
    '\n        Randomly crops image and mask in accord.\n        '
    cond_crop_image = tf.cast(tf.random.uniform([], maxval=2, dtype=tf.int32, seed=self.seed), tf.bool)
    shape = tf.cast(tf.shape(image), tf.float32)
    h = tf.cast((shape[0] * self.crop_percent), tf.int32)
    w = tf.cast((shape[1] * self.crop_percent), tf.int32)
    comb_tensor = tf.concat([image, mask], axis=2)
    comb_tensor = tf.cond(cond_crop_image, (lambda : tf.image.random_crop(comb_tensor, [h, w, (self.channels[0] + self.channels[1])], seed=self.seed)), (lambda : tf.identity(comb_tensor)))
    (image, mask) = tf.split(comb_tensor, [self.channels[0], self.channels[1]], axis=2)
    return (image, mask)
