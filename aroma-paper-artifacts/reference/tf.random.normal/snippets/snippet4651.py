from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import time
from absl import logging
import numpy as np
import tensorflow.compat.v1 as tf
from tensorflow_probability import bijectors as tfb
from tensorflow_probability import distributions as tfd
from tensorflow_probability import edward2 as ed
from tensorflow_probability.python.experimental.edward2.generated_random_variables import Normal
from tensorflow_probability.python.experimental.edward2.interceptor import tape
from tensorflow_probability.python.experimental.edward2.program_transformations import make_log_joint_fn
from tensorflow.python.ops.parallel_for import pfor
import program_transformations as program_transformations
import __builtin__
import builtins as __builtin__


def get_or_init(name, a, b, L=None, std_mean=None, prior_mean=None, prior_scale=None, shape=None):
    loc_name = (name + '_loc')
    scale_name = (name + '_scale')
    if ((loc_name in variational_parameters.keys()) and (scale_name in variational_parameters.keys())):
        return (variational_parameters[loc_name], variational_parameters[scale_name])
    else:
        pre_loc = tf.compat.v1.get_variable(name=loc_name, initializer=(0.01 * tf.random.normal(shape, dtype=tf.float32)))
        pre_scale = tf.nn.softplus(tf.compat.v1.get_variable(name=scale_name, initializer=((- 2) * tf.ones(shape, dtype=tf.float32))))
        variational_parameters[loc_name] = ((a + 0.1) * pre_loc)
        variational_parameters[scale_name] = (pre_scale ** (b + 0.1))
        return (variational_parameters[loc_name], variational_parameters[scale_name])
