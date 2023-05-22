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


def random_func():
    cand = []
    if (len(self.keep_top_k[self.select_num]) > 0):
        cand = list(choice(self.keep_top_k[self.select_num]))
    for i in range(len(cand)):
        if (np.random.random_sample() < m_prob):
            k = np.random.randint(len(self.operations[i]))
            cand[i] = self.operations[i][k]
    return tuple(list(cand))
