import torch
import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo


def pyramidal_make_layer(self, block, block_depth, stride=1):
    downsample = None
    if (stride != 1):
        downsample = nn.AvgPool2d((2, 2), stride=(2, 2), ceil_mode=True)
    layers = []
    self.featuremap_dim = (self.featuremap_dim + self.addrate)
    layers.append(block(self.input_featuremap_dim, int(round(self.featuremap_dim)), stride, downsample))
    for i in range(1, block_depth):
        temp_featuremap_dim = (self.featuremap_dim + self.addrate)
        layers.append(block((int(round(self.featuremap_dim)) * block.outchannel_ratio), int(round(temp_featuremap_dim)), 1))
        self.featuremap_dim = temp_featuremap_dim
    self.input_featuremap_dim = (int(round(self.featuremap_dim)) * block.outchannel_ratio)
    return nn.Sequential(*layers)
