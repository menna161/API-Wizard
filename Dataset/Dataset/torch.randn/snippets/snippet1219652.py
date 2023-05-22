import torch
from torch import nn
from torch.nn import functional as F
import numpy as np
from lib.utils.vis_logger import logger
from math import pi, sqrt, log
from math import pi, sqrt, log

if (__name__ == '__main__'):
    net = IODINE(3, 3, 128)
    (H, W) = (32, 32)
    B = 4
    x = torch.randn(B, 3, H, W)
    for i in range(5):
        loss = net(x)
        loss.backward()
