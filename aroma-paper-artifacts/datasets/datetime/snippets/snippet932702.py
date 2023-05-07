from __future__ import division
import math
import os
import datetime
import pprint
import scipy.misc
import numpy as np
import pretty_midi as pm
import copy
import config
import write_midi
import tensorflow as tf
from imageio import imread as _imread


def merge(images, size):
    (h, w) = (images.shape[1], images.shape[2])
    img = np.zeros(((h * size[0]), (w * size[1]), 3))
    for (idx, image) in enumerate(images):
        i = (idx % size[1])
        j = (idx // size[1])
        img[((j * h):((j * h) + h), (i * w):((i * w) + w), :)] = image
    return img
