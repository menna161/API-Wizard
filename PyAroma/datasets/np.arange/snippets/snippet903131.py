from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import os
import numpy as np
import torch
import numbers
import random
import tensorflow as tf
import mxnet as mx
from scipy.special import gammainc


def to_categorical(labels, nb_classes=None):
    '\n    Convert an array of labels to binary class matrix.\n\n    :param labels: An array of integer labels of shape `(nb_samples,)`\n    :type labels: `np.ndarray`\n    :param nb_classes: The number of classes (possible labels)\n    :type nb_classes: `int`\n    :return: A binary matrix representation of `y` in the shape `(nb_samples, nb_classes)`\n    :rtype: `np.ndarray`\n    '
    labels = np.array(labels, dtype=np.int32)
    if (not nb_classes):
        nb_classes = (np.max(labels) + 1)
    categorical = np.zeros((labels.shape[0], nb_classes), dtype=np.float32)
    categorical[(np.arange(labels.shape[0]), np.squeeze(labels))] = 1
    return categorical
