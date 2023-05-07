import tensorflow as tf
from tensorflow.keras import layers


def build(self, input_shape):
    '\n        initialize embedding_weights, where\n        id 0 is reserved for UNK, and its embedding fix to all zeros\n        '
    with tf.compat.v1.variable_scope(self.scope_name):
        unknown_id = tf.Variable(tf.zeros_initializer()([1, self.output_dim]), name='-'.join([self.layer_name, 'unknown']), trainable=False)
        normal_ids = tf.compat.v1.get_variable('-'.join([self.layer_name, 'normal']), [(self.input_dim - 1), self.output_dim], initializer=(tf.random_uniform_initializer(minval=(- self.initial_range), maxval=self.initial_range) if self.initial_range else None))
    self.embeddings = tf.concat([unknown_id, normal_ids], axis=0)
