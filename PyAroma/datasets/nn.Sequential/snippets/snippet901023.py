import math
import argparse
import time
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torchmeta.datasets.helpers import omniglot, miniimagenet
from torchmeta.utils.data import BatchMetaDataLoader
import higher
import hypergrad as hg


def conv_layer(ic, oc):
    return nn.Sequential(nn.Conv2d(ic, oc, 3, padding=1), nn.ReLU(inplace=True), nn.MaxPool2d(2), nn.BatchNorm2d(oc, momentum=1.0, affine=True, track_running_stats=False))
