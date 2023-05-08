import torch
import torch.nn as nn


def __init__(self, n_layers, ef_dim=32, z_dim=128):
    super(Encoder3D, self).__init__()
    model = []
    in_channels = 1
    out_channels = ef_dim
    for i in range((n_layers - 1)):
        model.append(nn.Conv3d(in_channels, out_channels, kernel_size=(4, 4, 4), stride=(2, 2, 2), padding=1, bias=False))
        model.append(nn.BatchNorm3d(num_features=out_channels, momentum=0.1))
        model.append(nn.LeakyReLU(0.02))
        in_channels = out_channels
        out_channels *= 2
    model.append(nn.Conv3d((out_channels // 2), z_dim, kernel_size=(4, 4, 4), stride=(1, 1, 1), padding=0))
    model.append(nn.Sigmoid())
    self.model = nn.Sequential(*model)
