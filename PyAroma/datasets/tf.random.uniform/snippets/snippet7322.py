import tensorflow as tf
import numpy as np
import os
import cv2
import glob
from tqdm import tqdm


@tf.function
def _random_jitter(self, input_image, real_image):
    (input_image, real_image) = self._resize(input_image, real_image, 286, 286)
    (input_image, real_image) = self._random_crop(input_image, real_image)
    if (tf.random.uniform(()) > 0.5):
        input_image = tf.image.flip_left_right(input_image)
        real_image = tf.image.flip_left_right(real_image)
    return (input_image, real_image)
