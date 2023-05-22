import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init
from torch.autograd import Variable
from core.config import cfg
import nn as mynn
import utils.net as net_utils


def _init_weights(self):

    def _init(m):
        if isinstance(m, nn.Conv2d):
            mynn.init.MSRAFill(m.weight)
            init.constant_(m.bias, 0)
        elif isinstance(m, nn.Linear):
            mynn.init.XavierFill(m.weight)
            init.constant_(m.bias, 0)
    self.apply(_init)
