import warnings
from collections import namedtuple
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils import model_zoo
import scipy.stats as stats


def _initialize_weights(self):
    for m in self.modules():
        if (isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear)):
            import scipy.stats as stats
            X = stats.truncnorm((- 2), 2, scale=0.01)
            values = torch.as_tensor(X.rvs(m.weight.numel()), dtype=m.weight.dtype)
            values = values.view(m.weight.size())
            with torch.no_grad():
                m.weight.copy_(values)
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
