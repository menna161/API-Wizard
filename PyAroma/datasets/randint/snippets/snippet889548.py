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


def validate(epoch, val_loader, model, criterion, args):
    batch_time = AverageMeter('Time', ':6.3f')
    losses = AverageMeter('Loss', ':.4e')
    top1 = AverageMeter('Acc@1', ':6.2f')
    top5 = AverageMeter('Acc@5', ':6.2f')
    progress = ProgressMeter(len(val_loader), [batch_time, losses, top1, top5], prefix='Test: ')
    model.eval()
    scale_ids = np.random.randint(low=0, high=len(channel_scale), size=13)
    with torch.no_grad():
        end = time.time()
        for (i, (images, target)) in enumerate(val_loader):
            images = images.cuda()
            target = target.cuda()
            logits = model(images, scale_ids)
            loss = criterion(logits, target)
            (pred1, pred5) = accuracy(logits, target, topk=(1, 5))
            n = images.size(0)
            losses.update(loss.item(), n)
            top1.update(pred1[0], n)
            top5.update(pred5[0], n)
            batch_time.update((time.time() - end))
            end = time.time()
            if ((i % args.print_freq) == 0):
                progress.display(i)
        print(' * Acc@1 {top1.avg:.3f} Acc@5 {top5.avg:.3f}'.format(top1=top1, top5=top5))
    return (losses.avg, top1.avg, top5.avg)
