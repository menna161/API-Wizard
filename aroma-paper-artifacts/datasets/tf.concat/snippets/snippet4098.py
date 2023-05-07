import tensorflow as tf
from absl import flags
from deepray.base.layers.interactions import SelfAttentionNet
from deepray.model.model_ctr import BaseCTRModel


def build_network(self, features, is_training=None):
    '\n\n        :param features:\n        :param is_training:\n        :return:\n        '
    deep_part = self.deep_block(features, is_training=is_training)
    attention_part = self.attention_block(features, is_training=is_training)
    logit = tf.concat([attention_part, deep_part], (- 1))
    return logit
