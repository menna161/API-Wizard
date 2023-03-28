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


def get_random_extend(num, op_flops_dict, extend_operator, vis_dict, ops):

    def get_random_cand_(extend_operator, ops):
        (layer, extend_op) = extend_operator
        rng = []
        for (i, op) in enumerate(ops):
            if ((i == layer) and (extend_op is not None)):
                select_op = extend_op
            elif (len(op) == 1):
                select_op = op[0]
            else:
                if ((- 1) in op):
                    assert (op[(- 1)] == (- 1))
                    k = np.random.randint((len(op) - 1))
                else:
                    k = np.random.randint(len(op))
                select_op = op[k]
            rng.append(select_op)
        rng = get_depth_full_rngs(ops, rng, layer)
        return tuple(rng)
    max_iters = (num * 100)
    candidates = []
    i = 0
    while ((i < num) and (max_iters > 0)):
        max_iters -= 1
        cand = get_random_cand_(extend_operator, ops)
        if (not legal(cand, op_flops_dict, vis_dict)):
            continue
        candidates.append(cand)
        i += 1
        print('random {}/{}'.format(len(candidates), num))
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} random_num = {}'.format(now, len(candidates)))
    return candidates
