import torch
from torch import nn
from torch.nn import functional as F
import numpy as np
from lib.utils.vis_logger import logger
from math import pi, sqrt, log
from math import pi, sqrt, log


def sample(self):
    '\n        Sample from current mean and dev\n        :return: return size is the same as self.mean\n        '
    logdev = (0.5 * self.logvar)
    dev = torch.exp(logdev)
    epsilon = torch.randn_like(self.mean, device=self.mean.device)
    return (self.mean + (dev * epsilon))
