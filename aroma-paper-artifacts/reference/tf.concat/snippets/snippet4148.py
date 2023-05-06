import tensorflow as tf
from absl import flags
from deepray.base.layers.core import Linear
from deepray.model.model_ctr import BaseCTRModel


def build_network(self, features, is_training=None):
    (wide_part, deep_part) = (features[0], features[1])
    deep_part = self.deep_block(deep_part, is_training=is_training)
    wide_part = self.wide_block(wide_part, is_training=is_training)
    logit = tf.concat([wide_part, deep_part], (- 1))
    return logit
