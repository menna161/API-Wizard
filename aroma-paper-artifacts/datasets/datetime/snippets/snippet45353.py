from __future__ import print_function
import os
import argparse
import torch.backends.cudnn as cudnn
from ssd import build_ssd
from utils import draw_boxes, helpers, save_boxes
import logging
import time
import datetime
from torch.autograd import Variable
from torchvision import datasets, transforms
from torch.utils.data import Dataset, DataLoader
from data import *
import shutil
import torch.nn as nn


def test_net_batch(args, net, gpu_id, dataset, transform, thresh):
    '\n    Batch testing\n    '
    num_images = len(dataset)
    if (args.limit != (- 1)):
        num_images = args.limit
    data_loader = DataLoader(dataset, args.batch_size, num_workers=args.num_workers, shuffle=False, collate_fn=detection_collate, pin_memory=True)
    total = len(dataset)
    logging.debug('Test dataset size is {}'.format(total))
    done = 0
    for (batch_idx, (images, targets, metadata)) in enumerate(data_loader):
        done = (done + len(images))
        logging.debug('processing {}/{}'.format(done, total))
        if args.cuda:
            images = images.cuda()
            targets = [ann.cuda() for ann in targets]
        else:
            images = Variable(images)
            targets = [Variable(ann, volatile=True) for ann in targets]
        (y, debug_boxes, debug_scores) = net(images)
        detections = y.data
        k = 0
        for (img, meta) in zip(images, metadata):
            img_id = meta[0]
            x_l = meta[1]
            y_l = meta[2]
            img = img.permute(1, 2, 0)
            scale = torch.Tensor([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])
            recognized_boxes = []
            recognized_scores = []
            i = 1
            j = 0
            while ((j < detections.size(2)) and (detections[(k, i, j, 0)] >= thresh)):
                score = detections[(k, i, j, 0)]
                pt = (detections[(k, i, j, 1:)] * args.window).cpu().numpy()
                coords = ((pt[0] + x_l), (pt[1] + y_l), (pt[2] + x_l), (pt[3] + y_l))
                recognized_boxes.append(coords)
                recognized_scores.append(score.cpu().numpy())
                j += 1
            save_boxes(args, recognized_boxes, recognized_scores, img_id)
            k = (k + 1)
            if args.verbose:
                draw_boxes(args, img.cpu().numpy(), recognized_boxes, recognized_scores, debug_boxes, debug_scores, scale, img_id)
