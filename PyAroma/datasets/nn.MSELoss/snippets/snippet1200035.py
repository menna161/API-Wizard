import torch
import torch.nn as nn
from torch.nn import init
import functools
from torch.optim import lr_scheduler
from deeplab import Deeplab
from collections import OrderedDict
import torch.nn.functional as F
from fcn8s_LSD import FCN8s_LSD


def __init__(self, use_lsgan=True, target_real_label=1.0, target_fake_label=0.0):
    super(GANLoss, self).__init__()
    self.register_buffer('real_label', torch.tensor(target_real_label))
    self.register_buffer('fake_label', torch.tensor(target_fake_label))
    if use_lsgan:
        self.loss = nn.MSELoss()
    else:
        self.loss = nn.BCELoss()
