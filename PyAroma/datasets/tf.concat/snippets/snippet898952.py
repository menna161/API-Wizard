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


def _make_library(predicted_dict, predictor_fn, observed_dict, eval_batch_size, similarity_provider, name='library'):
    'Make idempotent [num_elements, library_entry_length] library Tensor.'

    def _get_library_shape(predicted_dict, observed_library):
        'Infer the shape of the library from the observed and predicted data.'
        if (observed_library is None):
            prediction_shape = util.get_static_shape_without_adding_ops(predicted_dict, predictor_fn)
            library_entry_length = prediction_shape[1]
            num_elements_observed = 0
        else:
            (num_elements_observed, library_entry_length) = observed_library.shape.as_list()
            assert (num_elements_observed is not None), 'batch_size must be statically inferrable for the observed data.'
        num_elements = num_elements_observed
        if (predicted_dict is not None):
            num_elements_predicted = tf.contrib.framework.nest.flatten(predicted_dict)[0].shape[0]
            assert (num_elements_predicted is not None), 'batch_size must be statically inferrable for the predicted data.'
            num_elements += num_elements_predicted
        return [num_elements, library_entry_length]
    if (observed_dict is not None):
        observed_library = observed_dict[_KEY_FOR_LIBRARY_VECTORS]
    else:
        observed_library = None
    if (predicted_dict is not None):
        library_shape = _get_library_shape(predicted_dict, observed_library)

        def make_value_op():
            return tf.get_local_variable(name=name, shape=library_shape, dtype=tf.float32, initializer=tf.zeros_initializer)

        def make_init_op(value_op):
            prediction = util.map_predictor(predicted_dict, predictor_fn, sub_batch_size=eval_batch_size)
            if (observed_dict is not None):
                library = tf.concat([prediction, observed_library], axis=0)
            else:
                library = prediction
            normalized_library = similarity_provider.preprocess_library(library)
            return value_op.assign(normalized_library)
        full_library = util.value_op_with_initializer(make_value_op, make_init_op)
    else:
        full_library = similarity_provider.preprocess_library(observed_library)

    def _get_ids_fingerprints_and_masses(data_dict):
        if (data_dict is None):
            return ([], [], [])
        ids = data_dict[fmap_constants.INCHIKEY]
        if (ids.shape[0] == 0):
            return ([], [], [])
        fingerprints = data_dict[FP_NAME_FOR_JACCARD_SIMILARITY]
        masses = tf.squeeze(data_dict[fmap_constants.MOLECULE_WEIGHT], axis=1)
        return ([ids], [fingerprints], [masses])
    (predicted_ids, predicted_fingerprints, predicted_masses) = _get_ids_fingerprints_and_masses(predicted_dict)
    (observed_ids, observed_fingerprints, observed_masses) = _get_ids_fingerprints_and_masses(observed_dict)
    full_library_ids = tf.concat((predicted_ids + observed_ids), axis=0)
    full_fingerprints = tf.concat((predicted_fingerprints + observed_fingerprints), axis=0)
    full_masses = tf.concat((predicted_masses + observed_masses), axis=0)
    return (full_library, full_library_ids, full_fingerprints, full_masses)
