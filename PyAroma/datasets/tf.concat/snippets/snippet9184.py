import tensorflow as tf
import math
import constants as const
import numpy as np
import imageio
from pydoc import locate
from tensorflow.python.ops import control_flow_ops


def cshift(values):
    return tf.concat([values[((- 1):, ...)], values[(:(- 1), ...)]], 0)
