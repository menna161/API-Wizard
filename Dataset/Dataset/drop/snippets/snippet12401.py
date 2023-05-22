import torch
import torch.nn as nn
import math
from FastAutoAugment.networks.shakedrop import ShakeDrop


def forward(self, x):
    out = self.bn1(x)
    out = self.conv1(out)
    out = self.bn2(out)
    out = self.relu(out)
    out = self.conv2(out)
    out = self.bn3(out)
    out = self.relu(out)
    out = self.conv3(out)
    out = self.bn4(out)
    out = self.shake_drop(out)
    if (self.downsample is not None):
        shortcut = self.downsample(x)
        featuremap_size = shortcut.size()[2:4]
    else:
        shortcut = x
        featuremap_size = out.size()[2:4]
    batch_size = out.size()[0]
    residual_channel = out.size()[1]
    shortcut_channel = shortcut.size()[1]
    if (residual_channel != shortcut_channel):
        padding = torch.autograd.Variable(torch.cuda.FloatTensor(batch_size, (residual_channel - shortcut_channel), featuremap_size[0], featuremap_size[1]).fill_(0))
        out += torch.cat((shortcut, padding), 1)
    else:
        out += shortcut
    return out
