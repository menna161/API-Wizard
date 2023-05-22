from __future__ import absolute_import
from torch import nn
from torch.nn import functional as F
from torch.nn import init
import torchvision


def __init__(self, depth, pretrained=True, cut_at_pooling=False, num_features=0, norm=False, dropout=0, num_classes=0, fixed_layer=True):
    super(ResNet, self).__init__()
    self.depth = depth
    self.pretrained = pretrained
    self.cut_at_pooling = cut_at_pooling
    if (depth not in ResNet.__factory):
        raise KeyError('Unsupported depth:', depth)
    self.base = ResNet.__factory[depth](pretrained=pretrained)
    if fixed_layer:
        fixed_names = []
        for (name, module) in self.base._modules.items():
            if (name == 'layer3'):
                assert (fixed_names == ['conv1', 'bn1', 'relu', 'maxpool', 'layer1', 'layer2'])
                break
            fixed_names.append(name)
            for param in module.parameters():
                param.requires_grad = False
    if (not self.cut_at_pooling):
        self.num_features = num_features
        self.norm = norm
        self.dropout = dropout
        self.has_embedding = (num_features > 0)
        self.num_classes = num_classes
        out_planes = self.base.fc.in_features
        if self.has_embedding:
            self.feat = nn.Linear(out_planes, self.num_features)
            self.feat_bn = nn.BatchNorm1d(self.num_features)
            init.kaiming_normal(self.feat.weight, mode='fan_out')
            init.constant(self.feat.bias, 0)
            init.constant(self.feat_bn.weight, 1)
            init.constant(self.feat_bn.bias, 0)
        else:
            self.num_features = out_planes
        if (self.dropout > 0):
            self.drop = nn.Dropout(self.dropout)
        if (self.num_classes > 0):
            self.classifier = nn.Linear(self.num_features, self.num_classes)
            init.normal(self.classifier.weight, std=0.001)
            init.constant(self.classifier.bias, 0)
    if (not self.pretrained):
        self.reset_params()
