import argparse
import os
import shutil
import time
import sys
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
from torchvision import datasets, transforms
from torchsummaryX import summary
from pruned_model import resnet50
from ori_model import ori_resnet50
from math import cos, pi
import numpy as np
import yaml


def mixup_data(x, y, alpha=1.0, use_cuda=True):
    'Returns mixed inputs, pairs of targets, and lambda'
    if (alpha > 0):
        lam = np.random.beta(alpha, alpha)
    else:
        lam = 1
    batch_size = x.size()[0]
    if use_cuda:
        index = torch.randperm(batch_size).cuda()
    else:
        index = torch.randperm(batch_size)
    mixed_x = ((lam * x) + ((1 - lam) * x[(index, :)]))
    (y_a, y_b) = (y, y[index])
    return (mixed_x, y_a, y_b, lam)
