import os
import time
import numpy as np
import pickle
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from config import config
import sys
import functools
import copy
from utils import *


def get_depth_full_rngs(ops, rngs, layer):
    identity_locs = []
    for (i, op) in enumerate(ops):
        if (((- 1) in op) and (not (i == layer))):
            identity_locs.append(i)
    max_identity_num = len(identity_locs)
    identity_num = np.random.randint((max_identity_num + 1))
    select_identity = np.random.choice(identity_locs, identity_num, replace=False)
    select_identity = list(select_identity)
    for i in range(len(select_identity)):
        rngs[select_identity[i]] = (- 1)
    return rngs
