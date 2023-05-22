import torch
import torch.nn as nn
from operations import OPS, BN_OPS, NORMAL_OPS
import torch.nn.functional as F
import math
from dataset.config import widerface_640 as cfg


def __init__(self, genotype, feature_channel=256, weight_node=False, **kwargs):
    '\n        :param genotype:\n            The Genotype is formatted as follow:\n            [\n                # for a node\n                [\n                    # for an operation\n                    (prim, number of the front node)\n                    # other ops\n                    ...\n                ]\n                # other nodes\n                ...\n            ]\n        :param feature_channel:\n        '
    super(BiFPN_From_Genotype, self).__init__()
    bn = True
    if bn:
        ops = BN_OPS
        print('Retrain with BN - FPN.')
    else:
        ops = OPS
        print('Retrain without BN - FPN.')
    print(ops.keys())
    self.feature_channel = feature_channel
    self.genotype = genotype
    self.node_weights_enable = weight_node
    [self.conv1_td, self.conv1, self.conv2_td, self.conv2_du, self.conv2, self.conv3_td, self.conv3_du, self.conv3, self.conv4_td, self.conv4_du, self.conv4, self.conv5_td, self.conv5_du, self.conv5, self.conv6_du, self.conv6] = [ops[prim](feature_channel, 1, True) for node in self.genotype for (prim, _) in node]
    [self.w1, self.w2, self.w3, self.w4, self.w5, self.w6] = [nn.Parameter((0.001 * torch.randn(len(node)))) for node in self.genotype]
    self.out_layers = nn.ModuleList([nn.Conv2d(feature_channel, feature_channel, 1, 1, 0) for _ in range(6)])
