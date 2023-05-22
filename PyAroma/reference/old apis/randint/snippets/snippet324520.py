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


def get_random(self, num):
    print('random select ........')

    def get_random_cand():
        rng = []
        for (i, ops) in enumerate(self.operations):
            k = np.random.randint(len(ops))
            select_op = ops[k]
            rng.append(select_op)
        return tuple(rng)
    cand_iter = self.stack_random_cand(get_random_cand)
    max_iters = (num * 10000)
    while ((len(self.candidates) < num) and (max_iters > 0)):
        max_iters -= 1
        cand = next(cand_iter)
        if (not self.legal(cand)):
            continue
        self.candidates.append(cand)
        print('random {}/{}'.format(len(self.candidates), num))
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} random_num = {}'.format(now, len(self.candidates)))
