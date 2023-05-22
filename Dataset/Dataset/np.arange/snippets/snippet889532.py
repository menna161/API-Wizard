import os
import sys
import shutil
import pickle
import numpy as np
import time, datetime
import torch
import random
import logging
import argparse
import torch.nn as nn
import torch.utils
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.utils.data.distributed
import model_for_FLOPs
from utils.utils import *
from cal_FLOPs import print_model_parm_flops
from torchvision import datasets, transforms
from torch.autograd import Variable
from mobilenet_v1 import MobileNetV1, channel_scale


def get_mutation(keep_top_k, num_states, mutation_num, m_prob, test_dict, untest_dict):
    print('mutation ......', flush=True)
    res = []
    k = len(keep_top_k)
    iter = 0
    max_iters = 10
    while ((len(res) < mutation_num) and (iter < max_iters)):
        ids = np.random.choice(k, mutation_num)
        select_seed = np.array([keep_top_k[id] for id in ids])
        is_m = np.random.choice(np.arange(0, 2), (mutation_num, (num_states + 1)), p=[(1 - m_prob), m_prob])
        mu_val = (np.random.choice(np.arange(1, len(channel_scale)), (mutation_num, (num_states + 1))) * is_m)
        select_list = ((select_seed + mu_val) % len(channel_scale))
        iter += 1
        for can in select_list:
            t_can = tuple(can[:(- 1)])
            flops = print_model_parm_flops(model_for_flops, can[:(- 1)].astype(np.int))
            if ((t_can in untest_dict.keys()) or (t_can in test_dict.keys()) or (flops > max_FLOPs)):
                continue
            can[(- 1)] = flops
            res.append(can)
            untest_dict[t_can] = flops
            if (len(res) == mutation_num):
                break
    print('mutation_num = {}'.format(len(res)), flush=True)
    return res
