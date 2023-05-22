from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import inspect
import six
import tensorflow.compat.v1 as tf
from tensorflow_probability import distributions as tfd
from tensorflow_probability import bijectors as tfb
from tensorflow_probability.python.experimental.edward2.generated_random_variables import Normal
from tensorflow_probability.python.experimental.edward2.interceptor import interceptable
from tensorflow_probability.python.experimental.edward2.interceptor import interception
from tensorflow_probability.python import edward2
from tensorflow_probability.python.internal import prefer_static


def get_or_init(name, shape=None):
    loc_name = (name + '_loc')
    scale_name = (name + '_scale')
    if ((loc_name in variational_parameters.keys()) and (scale_name in variational_parameters.keys())):
        return (variational_parameters[loc_name], variational_parameters[scale_name])
    else:
        variational_parameters[loc_name] = tf.get_variable(name=loc_name, initializer=(0.01 * tf.random.normal(shape, dtype=tf.float32)))
        variational_parameters[scale_name] = tf.nn.softplus(tf.get_variable(name=scale_name, initializer=((- 2) * tf.ones(shape, dtype=tf.float32))))
        return (variational_parameters[loc_name], variational_parameters[scale_name])
