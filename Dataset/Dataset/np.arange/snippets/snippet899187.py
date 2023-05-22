from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tempfile
from absl.testing import absltest
from absl.testing import parameterized
import util
import numpy as np
import tensorflow as tf


def test_run_graph_and_process_results(self):
    batch_size = 3
    num_batches = 5
    with tf.Graph().as_default():
        _ = self._make_model(batch_size=batch_size, num_batches=num_batches, variable_initializer_value=2.0)
        saver = tf.train.Saver(tf.trainable_variables())
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver.save(sess, (self.temp_dir + '/model-'))
    with tf.Graph().as_default():
        ops_to_fetch = self._make_model(batch_size=batch_size, num_batches=num_batches, variable_initializer_value=3.0)
        results = []

        def process_fetched_values_fn(np_array):
            results.append(np_array)
        model_checkpoint_path = self.temp_dir
        util.run_graph_and_process_results(ops_to_fetch, model_checkpoint_path, process_fetched_values_fn)
        results = np.concatenate(results, axis=0)
        expected_results = (np.arange((num_batches * batch_size)) * 2.0)
        self.assertAllEqual(results, expected_results)
