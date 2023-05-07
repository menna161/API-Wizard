import torch.nn as nn
import torch.nn.functional as F
import math
from torch.nn import init


def forward(self, x):
    out = F.relu(self.bn1(x))
    shortcut = (self.shortcut(out) if hasattr(self, 'shortcut') else x)
    out = self.conv1(out)
    if (self.drop is not None):
        out = self.drop(out)
    out = self.conv2(F.relu(self.bn2(out)))
    out += shortcut
    return out
