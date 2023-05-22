import typing
import tensorflow as tf
from keras import backend as K
from keras.engine import Layer
from keras.layers import Permute
from keras.layers import Reshape
from keras import activations
from keras import initializers


def softmax_by_row(self, z: typing.Any) -> tuple:
    'Conduct softmax on each dimension across the four gates.'
    z_transform = Permute((2, 1))(Reshape((4, self._units))(z))
    size = [(- 1), 1, (- 1)]
    for i in range(0, self._units):
        begin = [0, i, 0]
        z_slice = tf.slice(z_transform, begin, size)
        if (i == 0):
            z_s = tf.nn.softmax(z_slice)
        else:
            z_s = tf.concat([z_s, tf.nn.softmax(z_slice)], 1)
    (zi, zl, zt, zd) = tf.unstack(z_s, axis=2)
    return (zi, zl, zt, zd)
