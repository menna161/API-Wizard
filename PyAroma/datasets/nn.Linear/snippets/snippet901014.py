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


def get_cnn_miniimagenet(hidden_size, n_classes):

    def conv_layer(ic, oc):
        return nn.Sequential(nn.Conv2d(ic, oc, 3, padding=1), nn.ReLU(inplace=True), nn.MaxPool2d(2), nn.BatchNorm2d(oc, momentum=1.0, affine=True, track_running_stats=False))
    net = nn.Sequential(conv_layer(3, hidden_size), conv_layer(hidden_size, hidden_size), conv_layer(hidden_size, hidden_size), conv_layer(hidden_size, hidden_size), nn.Flatten(), nn.Linear(((hidden_size * 5) * 5), n_classes))
    initialize(net)
    return net
