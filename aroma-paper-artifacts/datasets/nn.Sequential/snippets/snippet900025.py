import torch
import torch.nn as nn


def __init__(self, n_layers, f_dim, z_dim):
    'With skip connection'
    super(ImDecoderSkipConnect, self).__init__()
    in_channels = (z_dim + 3)
    out_channels = (f_dim * (2 ** (n_layers - 2)))
    model = []
    for i in range((n_layers - 1)):
        if (i > 0):
            in_channels += (z_dim + 3)
        if (i < 4):
            model.append([nn.Linear(in_channels, out_channels), nn.Dropout(p=0.4), nn.LeakyReLU()])
        else:
            model.append([nn.Linear(in_channels, out_channels), nn.LeakyReLU()])
        in_channels = out_channels
        out_channels = (out_channels // 2)
    model.append([nn.Linear(in_channels, 1), nn.Sigmoid()])
    self.layer1 = nn.Sequential(*model[0])
    self.layer2 = nn.Sequential(*model[1])
    self.layer3 = nn.Sequential(*model[2])
    self.layer4 = nn.Sequential(*model[3])
    self.layer5 = nn.Sequential(*model[4])
    self.layer6 = nn.Sequential(*model[5])
