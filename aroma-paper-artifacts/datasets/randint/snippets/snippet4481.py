from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import os
import time
import numpy as np
import tensorflow.compat.v1 as tf
import tensorflow_probability as tfp
from tensorflow_probability import edward2 as ed
from tensorflow_probability.python import mcmc
import util
import interleaved
import program_transformations as ed_transforms
from tensorflow.python.ops.parallel_for import pfor


def gen_id():
    return np.random.randint(10000, 99999)
