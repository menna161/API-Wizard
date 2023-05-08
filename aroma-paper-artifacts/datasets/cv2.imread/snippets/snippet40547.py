import numpy as np
import os
import cv2
import tensorflow as tf
import tensorflow.contrib.slim as slim
import random
from glob import glob


def load_test_image(image_path, img_width, img_height, img_channel):
    if (img_channel == 1):
        img = cv2.imread(image_path, flags=cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(image_path, flags=cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, dsize=(img_width, img_height))
    if (img_channel == 1):
        img = np.expand_dims(img, axis=0)
        img = np.expand_dims(img, axis=(- 1))
    else:
        img = np.expand_dims(img, axis=0)
    img = ((img / 127.5) - 1)
    return img
