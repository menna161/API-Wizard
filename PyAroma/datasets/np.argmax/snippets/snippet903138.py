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


def compute_success(classifier, x_clean, labels, x_adv, targeted=False, batch_size=1):
    '\n    Compute the success rate of an attack based on clean samples, adversarial samples and targets or correct labels.\n\n    :param classifier: Classifier used for prediction.\n    :type classifier: :class:`.Classifier`\n    :param x_clean: Original clean samples.\n    :type x_clean: `np.ndarray`\n    :param labels: Correct labels of `x_clean` if the attack is untargeted, or target labels of the attack otherwise.\n    :type labels: `np.ndarray`\n    :param x_adv: Adversarial samples to be evaluated.\n    :type x_adv: `np.ndarray`\n    :param targeted: `True` if the attack is targeted. In that case, `labels` are treated as target classes instead of\n           correct labels of the clean samples.s\n    :type targeted: `bool`\n    :param batch_size: Batch size\n    :type batch_size: `int`\n    :return: Percentage of successful adversarial samples.\n    :rtype: `float`\n    '
    adv_preds = np.argmax(classifier.predict(x_adv, batch_size=batch_size), axis=1)
    if targeted:
        rate = (np.sum((adv_preds == np.argmax(labels, axis=1))) / x_adv.shape[0])
    else:
        preds = np.argmax(classifier.predict(x_clean, batch_size=batch_size), axis=1)
        rate = (np.sum((adv_preds != preds)) / x_adv.shape[0])
    return rate
