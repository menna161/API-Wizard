import tensorflow as tf
from deepray.base.layers.core import CustomDropout, DeepBlock, Linear


def call(self, queries, keys, values, is_training=True, **kwargs):
    if (self.num_units is None):
        num_units = queries.get_shape().as_list[(- 1)]
    Q = tf.keras.layers.Dense(self.num_units, activation=tf.nn.relu)(queries)
    K = tf.keras.layers.Dense(self.num_units, activation=tf.nn.relu)(keys)
    V = tf.keras.layers.Dense(self.num_units, activation=tf.nn.relu)(values)
    if self.has_residual:
        V_res = tf.keras.layers.Dense(self.num_units, activation=tf.nn.relu)(values)
    Q_ = tf.concat(tf.split(Q, self.num_heads, axis=2), axis=0)
    K_ = tf.concat(tf.split(K, self.num_heads, axis=2), axis=0)
    V_ = tf.concat(tf.split(V, self.num_heads, axis=2), axis=0)
    weights = tf.matmul(Q_, tf.transpose(K_, [0, 2, 1]))
    weights = (weights / (K_.get_shape().as_list()[(- 1)] ** 0.5))
    weights = tf.nn.softmax(weights)
    weights = CustomDropout(rate=(1 - self.dropout_keep_prob))(weights, is_training)
    outputs = tf.matmul(weights, V_)
    outputs = tf.concat(tf.split(outputs, self.num_heads, axis=0), axis=2)
    if self.has_residual:
        outputs += V_res
    outputs = tf.nn.relu(outputs)
    outputs = self.normalize(outputs)
    return outputs
