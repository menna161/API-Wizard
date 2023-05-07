import typing
import tensorflow as tf
from keras import backend as K
from keras.engine import Layer
from keras.layers import Permute
from keras.layers import Reshape
from keras import activations
from keras import initializers


def calculate_recurrent_unit(self, inputs: typing.Any, states: typing.Any, step: int, h: typing.Any) -> tuple:
    '\n        Calculate recurrent unit.\n\n        :param inputs: A TensorArray which contains interaction\n            between left text and right text.\n        :param states: A TensorArray which stores the hidden state\n            of every step.\n        :param step: Recurrent step.\n        :param h: Hidden state from last operation.\n        '
    i = tf.math.floordiv(step, tf.constant(self._text2_maxlen))
    j = tf.math.mod(step, tf.constant(self._text2_maxlen))
    h_diag = states.read(((i * (self._text2_maxlen + 1)) + j))
    h_top = states.read((((i * (self._text2_maxlen + 1)) + j) + 1))
    h_left = states.read((((i + 1) * (self._text2_maxlen + 1)) + j))
    s_ij = inputs.read(step)
    q = tf.concat([tf.concat([h_top, h_left], 1), tf.concat([h_diag, s_ij], 1)], 1)
    r = self._recurrent_activation(self._time_distributed_dense(self._wr, q, self._br))
    z = self._time_distributed_dense(self._wz, q, self._bz)
    (zi, zl, zt, zd) = self.softmax_by_row(z)
    h_ij_l = self._time_distributed_dense(self._w_ij, s_ij, self._b_ij)
    h_ij_r = K.dot((r * tf.concat([h_left, h_top, h_diag], 1)), self._U)
    h_ij_ = self._activation((h_ij_l + h_ij_r))
    h_ij = ((((zl * h_left) + (zt * h_top)) + (zd * h_diag)) + (zi * h_ij_))
    states = states.write(((((i + 1) * (self._text2_maxlen + 1)) + j) + 1), h_ij)
    h_ij.set_shape(h_top.get_shape())
    return (inputs, states, (step + 1), h_ij)
