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
from resnet import ResNet50, channel_scale


def get_crossover(keep_top_k, num_states, crossover_num, test_dict, untest_dict):
    print('crossover ......', flush=True)
    res = []
    k = len(keep_top_k)
    iter = 0
    max_iters = (10 * crossover_num)
    while ((len(res) < crossover_num) and (iter < max_iters)):
        (id1, id2) = np.random.choice(k, 2, replace=False)
        p1 = keep_top_k[id1]
        p2 = keep_top_k[id2]
        mask = np.random.randint(low=0, high=2, size=(num_states + 1)).astype(np.float32)
        can = ((p1 * mask) + (p2 * (1.0 - mask)))
        iter += 1
        t_can = tuple(can[:(- 1)])
        model_for_flops = model_for_FLOPs.resnet50(can[:(- 1)].astype(np.int)).cuda()
        flops = print_model_parm_flops(model_for_flops)
        if ((t_can in untest_dict.keys()) or (t_can in test_dict.keys()) or (flops > max_FLOPs) or (flops < min_FLOPs)):
            continue
        can[(- 1)] = flops
        res.append(can)
        untest_dict[t_can] = (- 1)
        if (len(res) == crossover_num):
            break
    print('crossover_num = {}'.format(len(res)), flush=True)
    return res
