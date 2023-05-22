import torch
import torch.nn as nn
import numpy as np


def layer_init(self):
    for layer in self.cnn:
        if isinstance(layer, (nn.Conv2d, nn.Linear)):
            nn.init.orthogonal_(layer.weight, gain=1)
            nn.init.constant_(layer.bias, val=0)
    for (name, param) in self.rnn.named_parameters():
        if ('weight' in name):
            nn.init.orthogonal_(param)
        elif ('bias' in name):
            nn.init.constant_(param, 0)
    nn.init.orthogonal_(self.critic_linear.weight, gain=1)
    nn.init.constant_(self.critic_linear.bias, val=0)
