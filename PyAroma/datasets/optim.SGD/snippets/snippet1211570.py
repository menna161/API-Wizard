import os
import random
import logging
import argparse
import torch
import torch.nn as nn
import torch.utils.data as data
import torch.nn.functional as F
from tqdm import tqdm
from math import ceil
import numpy as np
from distutils.version import LooseVersion
from tensorboardX import SummaryWriter
from torchvision.utils import make_grid
import sys
from utils.eval import Eval
from utils.train_helper import get_model
from datasets.cityscapes_Dataset import City_Dataset, City_DataLoader, inv_preprocess, decode_labels
from datasets.gta5_Dataset import GTA5_DataLoader
from datasets.synthia_Dataset import SYNTHIA_DataLoader
import shutil


def __init__(self, args, cuda=None, train_id='None', logger=None):
    self.args = args
    os.environ['CUDA_VISIBLE_DEVICES'] = self.args.gpu
    self.cuda = (cuda and torch.cuda.is_available())
    self.device = torch.device(('cuda' if self.cuda else 'cpu'))
    self.train_id = train_id
    self.logger = logger
    self.current_MIoU = 0
    self.best_MIou = 0
    self.best_source_MIou = 0
    self.current_epoch = 0
    self.current_iter = 0
    self.second_best_MIou = 0
    self.writer = SummaryWriter(self.args.checkpoint_dir)
    self.Eval = Eval(self.args.num_classes)
    self.loss = nn.CrossEntropyLoss(weight=None, ignore_index=(- 1))
    self.loss.to(self.device)
    (self.model, params) = get_model(self.args)
    self.model = nn.DataParallel(self.model, device_ids=[0])
    self.model.to(self.device)
    if (self.args.optim == 'SGD'):
        self.optimizer = torch.optim.SGD(params=params, momentum=self.args.momentum, weight_decay=self.args.weight_decay)
    elif (self.args.optim == 'Adam'):
        self.optimizer = torch.optim.Adam(params, betas=(0.9, 0.99), weight_decay=self.args.weight_decay)
    if (self.args.dataset == 'cityscapes'):
        self.dataloader = City_DataLoader(self.args)
    elif (self.args.dataset == 'gta5'):
        self.dataloader = GTA5_DataLoader(self.args)
    else:
        self.dataloader = SYNTHIA_DataLoader(self.args)
    self.dataloader.num_iterations = min(self.dataloader.num_iterations, ITER_MAX)
    print(self.args.iter_max, self.dataloader.num_iterations)
    self.epoch_num = (ceil((self.args.iter_max / self.dataloader.num_iterations)) if (self.args.iter_stop is None) else ceil((self.args.iter_stop / self.dataloader.num_iterations)))
