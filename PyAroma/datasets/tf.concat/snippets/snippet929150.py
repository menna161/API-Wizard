from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from tensorflow_probability import distributions as tfd
from dreamer import tools
from dreamer.models import base


def features_from_state(self, state):
    return tf.concat([state['sample'], state['belief']], (- 1))
