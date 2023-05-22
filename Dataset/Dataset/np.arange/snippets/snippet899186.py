from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tempfile
from absl.testing import absltest
from absl.testing import parameterized
import util
import numpy as np
import tensorflow as tf


def _make_model(self, batch_size, num_batches, variable_initializer_value):
    np_inputs = np.arange((batch_size * num_batches))
    np_inputs = np.float32(np_inputs)
    inputs = tf.data.Dataset.from_tensor_slices(np_inputs)
    inputs = inputs.batch(batch_size).make_one_shot_iterator().get_next()
    scale = tf.get_variable(name='scale', dtype=tf.float32, initializer=variable_initializer_value, trainable=True)
    output = (inputs * scale)
    return output
