import typing
import tensorflow as tf
from keras.engine import Layer


def call(self, inputs: list, **kwargs) -> typing.Any:
    '\n        The computation logic of DynamicPoolingLayer.\n\n        :param inputs: two input tensors.\n        '
    self._validate_dpool_size()
    (x, dpool_index) = inputs
    dpool_shape = tf.shape(dpool_index)
    batch_index_one = tf.expand_dims(tf.expand_dims(tf.range(dpool_shape[0]), axis=(- 1)), axis=(- 1))
    batch_index = tf.expand_dims(tf.tile(batch_index_one, [1, self._msize1, self._msize2]), axis=(- 1))
    dpool_index_ex = tf.concat([batch_index, dpool_index], axis=3)
    x_expand = tf.gather_nd(x, dpool_index_ex)
    stride1 = (self._msize1 // self._psize1)
    stride2 = (self._msize2 // self._psize2)
    x_pool = tf.nn.max_pool(x_expand, [1, stride1, stride2, 1], [1, stride1, stride2, 1], 'VALID')
    return x_pool
