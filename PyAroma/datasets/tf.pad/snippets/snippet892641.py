from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import copy
import tensorflow as tf
from collections import namedtuple
from tensorflow.python.util import nest


def inference_fn(inputs, state):
    local_features = {'source': features['source'], 'source_length': features['source_length'], 'target': tf.pad(inputs[(:, 1:)], [[0, 0], [0, 1]]), 'target_length': tf.fill([tf.shape(inputs)[0]], tf.shape(inputs)[1])}
    outputs = []
    next_state = []
    for (model_fn, model_state) in zip(model_fns, state):
        if model_state:
            (output, new_state) = model_fn(local_features, model_state)
            outputs.append(output)
            next_state.append(new_state)
        else:
            output = model_fn(local_features)
            outputs.append(output)
            next_state.append({})
    log_prob = (tf.add_n(outputs) / float(len(outputs)))
    return (log_prob, next_state)
