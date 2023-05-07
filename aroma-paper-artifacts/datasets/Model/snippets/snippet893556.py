import torch.nn as nn
from collections import OrderedDict
from torchmeta.modules import MetaModule, MetaConv2d, MetaBatchNorm2d, MetaSequential, MetaLinear


def ModelConvOmniglot(out_features, hidden_size=64):
    return MetaConvModel(1, out_features, hidden_size=hidden_size, feature_size=hidden_size)
