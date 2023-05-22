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
from mobilenet_v2 import MobileNetV2, overall_channel_scale, mid_channel_scale


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
        mask = []
        for i in range(len(stage_repeat)):
            mask += ([np.random.randint(low=0, high=2)] * stage_repeat[i])
        for i in range((num_states + 1)):
            mask += [np.random.randint(low=0, high=2)]
        mask = np.array(mask)
        can = ((p1 * mask) + (p2 * (1.0 - mask)))
        iter += 1
        t_can = can[:(- 1)]
        overall_scale_ids = t_can[:sum(stage_repeat)].astype(np.int)
        mid_scale_ids = t_can[sum(stage_repeat):].astype(np.int)
        model_for_flops = model_for_FLOPs.MobileNetV2(overall_scale_ids, mid_scale_ids).cuda()
        flops = print_model_parm_flops(model_for_flops)
        t_can = tuple(can[:(- 1)])
        if ((t_can in untest_dict.keys()) or (t_can in test_dict.keys()) or (flops > max_FLOPs)):
            continue
        can[(- 1)] = flops
        res.append(can)
        untest_dict[t_can] = (- 1)
        if (len(res) == crossover_num):
            break
    print('crossover_num = {}'.format(len(res)), flush=True)
    return res
