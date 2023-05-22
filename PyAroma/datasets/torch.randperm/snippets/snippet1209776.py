from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import _init_paths
import os
import sys
import numpy as np
import argparse
import pprint
import pdb
import time
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data.sampler import Sampler
from roi_data_layer.roidb import combined_roidb
from roi_data_layer.roibatchLoader import roibatchLoader
from model.utils.config import cfg, cfg_from_file, cfg_from_list, get_output_dir
from model.utils.net_utils import weights_normal_init, save_net, load_net, adjust_learning_rate, save_checkpoint, clip_gradient
from model.faster_rcnn.vgg16 import vgg16
from model.faster_rcnn.resnet import resnet
import itertools
import math
from tensorboardX import SummaryWriter


def __iter__(self):
    rand_num = (torch.randperm(self.num_per_batch).view((- 1), 1) * self.batch_size)
    self.rand_num = (rand_num.expand(self.num_per_batch, self.batch_size) + self.range)
    self.rand_num_view = self.rand_num.view((- 1))
    if self.leftover_flag:
        self.rand_num_view = torch.cat((self.rand_num_view, self.leftover), 0)
    return iter(self.rand_num_view)
