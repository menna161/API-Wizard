import argparse
import json
import math
import os
import random
import time
from os import path
import numpy as np
import torch
import torch.nn.init as init
import torch.optim as optim
from datasets import CartPoleDataset, PendulumDataset, PlanarDataset, ThreePoleDataset
from losses import curvature, nce_past
from pc3_model import PC3
from tensorboardX import SummaryWriter
from torch import nn
from torch.utils.data import DataLoader


def weights_init(m):
    if isinstance(m, nn.Linear):
        init.kaiming_uniform_(m.weight, a=math.sqrt(5))
        if (m.bias is not None):
            (fan_in, _) = init._calculate_fan_in_and_fan_out(m.weight)
            bound = (1 / math.sqrt(fan_in))
            init.uniform_(m.bias, (- bound), bound)
