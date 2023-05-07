import tensorflow as tf
from absl import flags
from deepray.model.model_ctr import BaseCTRModel


def build_network(self, features, is_training=None):
    '\n        TODO\n\n        :param features:\n        :param is_training:\n        :return:\n        '
    (ev_list, sparse_ev_list, fv_list) = features
    din_part = self.din_block(sparse_ev_list[self.flags.candidate_item], sparse_ev_list[self.flags.history_item], is_training)
    deep_part = self.mlp_block(self.concat((ev_list + fv_list)))
    logit = tf.concat(values=[din_part, deep_part], axis=1)
    return logit
