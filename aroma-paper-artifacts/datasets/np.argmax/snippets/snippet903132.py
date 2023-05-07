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


def random_targets(labels, nb_classes):
    '\n    Given a set of correct labels, randomly choose target labels different from the original ones. These can be\n    one-hot encoded or integers.\n\n    :param labels: The correct labels\n    :type labels: `np.ndarray`\n    :param nb_classes: The number of classes for this model\n    :type nb_classes: `int`\n    :return: An array holding the randomly-selected target classes, one-hot encoded.\n    :rtype: `np.ndarray`\n    '
    if (len(labels.shape) > 1):
        labels = np.argmax(labels, axis=1)
    result = np.zeros(labels.shape)
    for class_ind in range(nb_classes):
        other_classes = list(range(nb_classes))
        other_classes.remove(class_ind)
        in_cl = (labels == class_ind)
        result[in_cl] = np.random.choice(other_classes)
    return to_categorical(result, nb_classes)
