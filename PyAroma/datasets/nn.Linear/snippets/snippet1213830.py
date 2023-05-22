import torch
import torch.nn as nn
from torch.nn import functional as F
from ute.utils.arg_pars import opt
from ute.utils.logging_setup import logger


def _init_weights(self):
    for m in self.modules():
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, 0, 0.01)
            nn.init.constant_(m.bias, 0)
