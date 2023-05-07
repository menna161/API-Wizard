import os
import sys
import shutil
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
from utils.utils import *
from torchvision import datasets, transforms
from torch.autograd import Variable
from mobilenet_v1 import MobileNetV1, channel_scale


def train(epoch, train_loader, model, criterion, optimizer, scheduler):
    batch_time = AverageMeter('Time', ':6.3f')
    data_time = AverageMeter('Data', ':6.3f')
    losses = AverageMeter('Loss', ':.4e')
    top1 = AverageMeter('Acc@1', ':6.2f')
    top5 = AverageMeter('Acc@5', ':6.2f')
    progress = ProgressMeter(len(train_loader), [batch_time, data_time, losses, top1, top5], prefix='Epoch: [{}]'.format(epoch))
    model.train()
    end = time.time()
    scheduler.step()
    for (i, (images, target)) in enumerate(train_loader):
        data_time.update((time.time() - end))
        images = images.cuda()
        target = target.cuda()
        scale_ids = np.random.randint(low=0, high=len(channel_scale), size=13)
        logits = model(images, scale_ids)
        loss = criterion(logits, target)
        (prec1, prec5) = accuracy(logits, target, topk=(1, 5))
        n = images.size(0)
        losses.update(loss.item(), n)
        top1.update(prec1.item(), n)
        top5.update(prec5.item(), n)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        batch_time.update((time.time() - end))
        end = time.time()
        if ((i % args.print_freq) == 0):
            progress.display(i)
    return (losses.avg, top1.avg, top5.avg, epoch)
