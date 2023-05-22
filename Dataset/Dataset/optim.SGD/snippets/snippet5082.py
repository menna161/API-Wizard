import os
import torch
import torch.optim as optim
import logging
import numpy as np
import argparse
from torchvision.utils import make_grid
from tensorboardX import SummaryWriter
from . import dataloader


def get_opt(model, args):
    if (args.opt == 'adam'):
        optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    elif (args.opt == 'sgd'):
        optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=0.9, weight_decay=args.weight_decay)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=args.epoch, gamma=args.gamma)
    return (optimizer, scheduler)
