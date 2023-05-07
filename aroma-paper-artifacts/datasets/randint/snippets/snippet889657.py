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


def random_can(num, num_states, test_dict, untest_dict):
    print('random select ........', flush=True)
    candidates = []
    while (len(candidates) < num):
        can = np.random.randint(low=int((0.4 * len(channel_scale))), high=int((0.8 * len(channel_scale))), size=(num_states + 1)).astype(np.float32)
        t_can = tuple(can[:(- 1)])
        model_for_flops = model_for_FLOPs.resnet50(can[:(- 1)].astype(np.int)).cuda()
        flops = print_model_parm_flops(model_for_flops)
        print(flops, flush=True)
        if ((t_can in test_dict.keys()) or (t_can in untest_dict.keys()) or (flops > max_FLOPs) or (flops < min_FLOPs)):
            continue
        can[(- 1)] = flops
        candidates.append(can)
        untest_dict[t_can] = (- 1)
    print('random_num = {}'.format(len(candidates)), flush=True)
    return candidates
