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


def _marshal(*rvs):
    'Args: a list of ed.RandomVariables each with vector or scalar event shape\n  (which must be staticly known), and all having the same batch shape.\n\n  Returns: a Tensor from concatenating their values along a single vector\n  dimension.\n  '
    vector_rvs = []
    for rv in rvs:
        v = rv.value
        if (v.shape.ndims == 0):
            vector_rvs.append([v])
        else:
            vector_rvs.append(v)
    print(vector_rvs)
    return tf.concat(vector_rvs, axis=(- 1))
