from __future__ import print_function
import errno
import os
import re
import collections
import numpy as np
import operator
import functools
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch._six import string_classes
from torch.utils.data.dataloader import default_collate


def weights_init(m):
    'custom weights initialization.'
    cname = m.__class__
    if ((cname == nn.Linear) or (cname == nn.Conv2d) or (cname == nn.ConvTranspose2d)):
        m.weight.data.normal_(0.0, 0.02)
    elif (cname == nn.BatchNorm2d):
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)
    else:
        print(('%s is not initialized.' % cname))
