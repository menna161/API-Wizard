import os
import sys
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from super_model import SuperNetwork
from torch.autograd import Variable
from config import config
from test_server import TestClient
import copy
import functools
import pickle
import traceback


def get_random_cand():
    rng = []
    for (i, ops) in enumerate(self.operations):
        k = np.random.randint(len(ops))
        select_op = ops[k]
        rng.append(select_op)
    return tuple(rng)
