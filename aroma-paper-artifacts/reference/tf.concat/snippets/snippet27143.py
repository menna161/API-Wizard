import tensorflow as tf
from keras import backend as K
from keras.engine import Layer
from matchzoo.contrib.layers import DecayingDropoutLayer


def call(self, inputs, **kwargs):
    '\n        The computation logic of EncodingLayer.\n\n        :param inputs: an input tensor.\n        '
    x = (tf.expand_dims(inputs, 1) * 0)
    x = tf.transpose(x, (0, 1, 3, 2))
    mid = (x + tf.expand_dims(inputs, (- 1)))
    up = tf.transpose(mid, (0, 3, 2, 1))
    inputs_concat = tf.concat([up, mid, (up * mid)], axis=2)
    A = K.dot(self._w_itr_att, inputs_concat)
    SA = tf.nn.softmax(A, axis=2)
    itr_attn = K.batch_dot(SA, inputs)
    inputs_attn_concat = tf.concat([inputs, itr_attn], axis=2)
    concat_dropout = DecayingDropoutLayer(initial_keep_rate=self._initial_keep_rate, decay_interval=self._decay_interval, decay_rate=self._decay_rate)(inputs_attn_concat)
    z = tf.tanh((K.dot(concat_dropout, self._w1) + self._b1))
    r = tf.sigmoid((K.dot(concat_dropout, self._w2) + self._b2))
    f = tf.sigmoid((K.dot(concat_dropout, self._w3) + self._b3))
    encoding = ((r * inputs) + (f * z))
    return encoding
