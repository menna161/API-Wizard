import torch
import torch.nn as nn
import torch.nn.functional as F
import copy


def __init__(self, input_dim, mlp1=[10, 32, 64], pooling='mean_std', mlp2=[64, 128], with_extra=True, extra_size=4):
    "\n        Pixel-set encoder.\n        Args:\n            input_dim (int): Number of channels of the input tensors\n            mlp1 (list):  Dimensions of the successive feature spaces of MLP1\n            pooling (str): Pixel-embedding pooling strategy, can be chosen in ('mean','std','max,'min')\n                or any underscore-separated combination thereof.\n            mlp2 (list): Dimensions of the successive feature spaces of MLP2\n            with_extra (bool): Whether additional pre-computed features are passed between the two MLPs\n            extra_size (int, optional): Number of channels of the additional features, if any.\n        "
    super(PixelSetEncoder, self).__init__()
    self.input_dim = input_dim
    self.mlp1_dim = copy.deepcopy(mlp1)
    self.mlp2_dim = copy.deepcopy(mlp2)
    self.pooling = pooling
    self.with_extra = with_extra
    self.extra_size = extra_size
    self.name = 'PSE-{}-{}-{}'.format('|'.join(list(map(str, self.mlp1_dim))), pooling, '|'.join(list(map(str, self.mlp2_dim))))
    self.output_dim = ((input_dim * len(pooling.split('_'))) if (len(self.mlp2_dim) == 0) else self.mlp2_dim[(- 1)])
    inter_dim = (self.mlp1_dim[(- 1)] * len(pooling.split('_')))
    if self.with_extra:
        self.name += 'Extra'
        inter_dim += self.extra_size
    assert (input_dim == mlp1[0])
    assert (inter_dim == mlp2[0])
    layers = []
    for i in range((len(self.mlp1_dim) - 1)):
        layers.append(linlayer(self.mlp1_dim[i], self.mlp1_dim[(i + 1)]))
    self.mlp1 = nn.Sequential(*layers)
    layers = []
    for i in range((len(self.mlp2_dim) - 1)):
        layers.append(nn.Linear(self.mlp2_dim[i], self.mlp2_dim[(i + 1)]))
        layers.append(nn.BatchNorm1d(self.mlp2_dim[(i + 1)]))
        if (i < (len(self.mlp2_dim) - 2)):
            layers.append(nn.ReLU())
    self.mlp2 = nn.Sequential(*layers)
