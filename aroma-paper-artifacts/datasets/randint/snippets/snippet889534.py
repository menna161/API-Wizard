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


def random_can(num, num_states, test_dict, untest_dict):
    print('random select ........', flush=True)
    candidates = []
    while (len(candidates) < num):
        can = np.random.randint(low=0, high=len(channel_scale), size=(num_states + 1)).astype(np.float32)
        t_can = tuple(can[:(- 1)])
        flops = print_model_parm_flops(model_for_flops, can[:(- 1)].astype(np.int))
        if ((t_can in test_dict.keys()) or (t_can in untest_dict.keys()) or (flops > max_FLOPs)):
            continue
        can[(- 1)] = flops
        candidates.append(can)
        untest_dict[t_can] = (- 1)
    print('random_num = {}'.format(len(candidates)), flush=True)
    return candidates
