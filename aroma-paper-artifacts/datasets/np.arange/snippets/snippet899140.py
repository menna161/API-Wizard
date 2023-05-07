from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import abc
import numpy as np
import tensorflow as tf


def _make_weights(self, tensor):
    num_bins = tensor.shape[1].value
    weights = np.power(np.arange(1, (num_bins + 1)), self.hparams.mass_power)[(np.newaxis, :)]
    return (weights / np.sum(weights))
