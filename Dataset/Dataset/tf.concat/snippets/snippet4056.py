import tensorflow as tf
from absl import flags
from deepray.base.layers.core import DeepNet


def concat(self, inputs):
    return tf.concat(inputs, (- 1))
