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


def get_label_conf(y_vec):
    '\n    Returns the confidence and the label of the most probable class given a vector of class confidences\n    :param y_vec: (np.ndarray) vector of class confidences, nb of instances as first dimension\n    :return: (np.ndarray, np.ndarray) confidences and labels\n    '
    assert (len(y_vec.shape) == 2)
    (confs, labels) = (np.amax(y_vec, axis=1), np.argmax(y_vec, axis=1))
    return (confs, labels)
