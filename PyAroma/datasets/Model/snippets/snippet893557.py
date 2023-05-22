import torch.nn as nn
from collections import OrderedDict
from torchmeta.modules import MetaModule, MetaConv2d, MetaBatchNorm2d, MetaSequential, MetaLinear


def ModelConvMiniImagenet(out_features, hidden_size=64):
    return MetaConvModel(3, out_features, hidden_size=hidden_size, feature_size=((5 * 5) * hidden_size))
