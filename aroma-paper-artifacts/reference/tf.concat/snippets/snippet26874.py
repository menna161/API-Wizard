import typing
import tensorflow as tf
from keras.engine import Layer


def call(self, inputs: list, **kwargs) -> typing.Any:
    '\n        The computation logic of MatchingLayer.\n\n        :param inputs: two input tensors.\n        '
    x1 = inputs[0]
    x2 = inputs[1]
    if (self._matching_type == 'dot'):
        if self._normalize:
            x1 = tf.math.l2_normalize(x1, axis=2)
            x2 = tf.math.l2_normalize(x2, axis=2)
        return tf.expand_dims(tf.einsum('abd,acd->abc', x1, x2), 3)
    else:
        if (self._matching_type == 'mul'):

            def func(x, y):
                return (x * y)
        elif (self._matching_type == 'plus'):

            def func(x, y):
                return (x + y)
        elif (self._matching_type == 'minus'):

            def func(x, y):
                return (x - y)
        elif (self._matching_type == 'concat'):

            def func(x, y):
                return tf.concat([x, y], axis=3)
        else:
            raise ValueError(f'Invalid matching type.{self._matching_type} received.Mut be in `dot`, `mul`, `plus`, `minus` and `concat`.')
        x1_exp = tf.stack(([x1] * self._shape2[1]), 2)
        x2_exp = tf.stack(([x2] * self._shape1[1]), 1)
        return func(x1_exp, x2_exp)
