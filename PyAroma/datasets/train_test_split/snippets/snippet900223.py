import argparse
import os
from datetime import datetime
from os.path import join as pjoin
import itertools
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from tensorboardX import SummaryWriter
from torch.utils import data
from tqdm import tqdm
import core.loss
import torchvision.utils as vutils
from core.augmentations import Compose, RandomHorizontallyFlip, RandomRotate, AddNoise
from core.loader.data_loader import *
from core.metrics import runningScore
from core.models import get_model
from core.utils import np_to_tb


def split_train_val(args, per_val=0.1):
    loader_type = 'patch'
    labels = np.load(pjoin('data', 'train', 'train_labels.npy'))
    (iline, xline, depth) = labels.shape
    i_list = []
    horz_locations = range(0, (xline - args.stride), args.stride)
    vert_locations = range(0, (depth - args.stride), args.stride)
    for i in range(iline):
        locations = [[j, k] for j in horz_locations for k in vert_locations]
        patches_list = [((((('i_' + str(i)) + '_') + str(j)) + '_') + str(k)) for (j, k) in locations]
        i_list.append(patches_list)
    i_list = list(itertools.chain(*i_list))
    x_list = []
    horz_locations = range(0, (iline - args.stride), args.stride)
    vert_locations = range(0, (depth - args.stride), args.stride)
    for j in range(xline):
        locations = [[i, k] for i in horz_locations for k in vert_locations]
        patches_list = [((((('x_' + str(i)) + '_') + str(j)) + '_') + str(k)) for (i, k) in locations]
        x_list.append(patches_list)
    x_list = list(itertools.chain(*x_list))
    list_train_val = (i_list + x_list)
    (list_train, list_val) = train_test_split(list_train_val, test_size=per_val, shuffle=True)
    file_object = open(pjoin('data', 'splits', (loader_type + '_train_val.txt')), 'w')
    file_object.write('\n'.join(list_train_val))
    file_object.close()
    file_object = open(pjoin('data', 'splits', (loader_type + '_train.txt')), 'w')
    file_object.write('\n'.join(list_train))
    file_object.close()
    file_object = open(pjoin('data', 'splits', (loader_type + '_val.txt')), 'w')
    file_object.write('\n'.join(list_val))
    file_object.close()
