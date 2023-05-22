from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf


def lambda_return(reward, value, bootstrap, pcont, lambda_, axis, stop_gradient=True):
    assert (reward.shape.ndims == value.shape.ndims), (reward.shape, value.shape)
    dims = list(range(reward.shape.ndims))
    dims = ((([axis] + dims[1:axis]) + [0]) + dims[(axis + 1):])
    if isinstance(pcont, (int, float)):
        pcont = (pcont * tf.ones_like(reward))
    reward = tf.transpose(reward, dims)
    value = tf.transpose(value, dims)
    pcont = tf.transpose(pcont, dims)
    if (bootstrap is None):
        bootstrap = tf.zeros_like(value[(- 1)])
    next_values = tf.concat([value[1:], bootstrap[None]], 0)
    inputs = (reward + ((pcont * next_values) * (1 - lambda_)))
    return_ = tf.scan(fn=(lambda agg, cur: (cur[0] + ((cur[1] * lambda_) * agg))), elems=(inputs, pcont), initializer=bootstrap, back_prop=(not stop_gradient), reverse=True)
    return_ = tf.transpose(return_, dims)
    if stop_gradient:
        return_ = tf.stop_gradient(return_)
    return return_
