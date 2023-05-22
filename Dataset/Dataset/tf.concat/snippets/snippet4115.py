import tensorflow as tf
from deepray.model.model_fm import FactorizationMachine


def build_network(self, features, is_training=None):
    '\n\n        :param features:\n        :param is_training:\n        :return:\n        '
    fm_out = self.fm_block(features)
    deep_out = self.deep_block(features)
    logit = tf.concat([deep_out, fm_out], (- 1))
    return logit
