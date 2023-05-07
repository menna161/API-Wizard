import tensorflow as tf
from absl import flags
from deepray.base.layers.core import CustomDropout, DeepBlock
from deepray.base.layers.fwbi import FieldWiseBiInteraction
from deepray.model.model_ctr import BaseCTRModel


def build_network(self, features, is_training=None):
    '\n\n        :param features:\n        :param is_training:\n        :return:\n        '
    (ev_list, fv_list) = features
    deep_out = self.mlp_block(self.concat((ev_list + fv_list)))
    fwbi = self.fwbi(ev_list)
    fwbi_fc_32 = self.fwbi_fc_32(fwbi)
    fwbi_bn = self.fwbi_bn(fwbi_fc_32)
    fwbi_out = self.fwbi_drop(fwbi_bn)
    logit = tf.concat(values=[deep_out, fwbi_out], axis=1)
    return logit
