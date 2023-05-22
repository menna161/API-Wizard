import os
import sys
import time
import math
import numpy as np
from urllib.request import urlopen, Request
from PIL import Image
import torch.nn as nn
import torch.nn.init as init
from pathlib import Path
import io


def init_params(net):
    'Init layer parameters.'
    for m in net.modules():
        if isinstance(m, nn.Conv2d):
            init.kaiming_normal(m.weight, mode='fan_out')
            if m.bias:
                init.constant(m.bias, 0)
        elif isinstance(m, nn.BatchNorm2d):
            init.constant(m.weight, 1)
            init.constant(m.bias, 0)
        elif isinstance(m, nn.Linear):
            init.normal(m.weight, std=0.001)
            if m.bias:
                init.constant(m.bias, 0)
