from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import namedtuple
from os import path
import feature_map_constants as fmap_constants
import mass_spec_constants as ms_constants
import util
import numpy as np
import tensorflow as tf


def make_init_op(value_op):
    prediction = util.map_predictor(predicted_dict, predictor_fn, sub_batch_size=eval_batch_size)
    if (observed_dict is not None):
        library = tf.concat([prediction, observed_library], axis=0)
    else:
        library = prediction
    normalized_library = similarity_provider.preprocess_library(library)
    return value_op.assign(normalized_library)
