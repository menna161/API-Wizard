from data import *
from utils.augmentations import SSDAugmentation
from layers.modules import MultiBoxLoss
from ssd import build_ssd
import os
import sys
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn
import torch.nn.init as init
import torch.utils.data as data
import argparse
from utils import helpers
import logging
import time
import datetime
from torchviz import make_dot
import visdom


def validate(args, net, criterion, cfg):
    validation_batch_size = 1
    try:
        net.eval()
        dataset = GTDBDetection(args, args.validation_data, split='validate', transform=SSDAugmentation(cfg['min_dim'], mean=MEANS))
        data_loader = data.DataLoader(dataset, validation_batch_size, num_workers=args.num_workers, shuffle=False, collate_fn=detection_collate, pin_memory=True)
        total = len(dataset)
        done = 0
        loc_loss = 0
        conf_loss = 0
        start = time.time()
        for (batch_idx, (images, targets, ids)) in enumerate(data_loader):
            done = (done + len(images))
            logging.debug('processing {}/{}'.format(done, total))
            if args.cuda:
                images = images.cuda()
                targets = [ann.cuda() for ann in targets]
            else:
                images = Variable(images)
                targets = [Variable(ann, volatile=True) for ann in targets]
            y = net(images)
            (loss_l, loss_c) = criterion(y, targets)
            loc_loss += loss_l.item()
            conf_loss += loss_c.item()
        end = time.time()
        logging.debug(('Time taken for validation ' + str(datetime.timedelta(seconds=(end - start)))))
        return ((loc_loss + conf_loss) / (total / validation_batch_size))
    except Exception as e:
        logging.error('Could not validate', exc_info=True)
        return 0
