from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import abc
import functools
from os import path
import feature_map_constants as fmap_constants
import library_matching
import mass_spec_constants as ms_constants
import parse_sdf_utils
import plot_spectra_utils
import similarity as similarity_lib
import util
import numpy as np
import tensorflow as tf


def _mask_prediction_by_mass(self, raw_prediction, feature_dict, hparams):
    'Zero out predictions to the right of the maximum possible mass.'
    total_mass = feature_dict[fmap_constants.MOLECULE_WEIGHT][(..., 0)]
    total_mass = tf.cast(tf.round(total_mass), dtype=tf.int32)
    indices = np.arange(raw_prediction.shape[(- 1)].value)[(np.newaxis, ...)]
    right_of_total_mass = (indices > (total_mass[(..., tf.newaxis)] + hparams.max_prediction_above_molecule_mass))
    return tf.where(right_of_total_mass, tf.zeros_like(raw_prediction), raw_prediction)
