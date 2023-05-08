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
from mobilenet_v2 import MobileNetV2, mid_channel_scale, overall_channel_scale


def main():
    if (not torch.cuda.is_available()):
        sys.exit(1)
    start_t = time.time()
    cudnn.benchmark = True
    cudnn.enabled = True
    logging.info('args = %s', args)
    model = MobileNetV2()
    logging.info(model)
    model = nn.DataParallel(model).cuda()
    criterion = nn.CrossEntropyLoss()
    criterion = criterion.cuda()
    criterion_smooth = CrossEntropyLabelSmooth(CLASSES, args.label_smooth)
    criterion_smooth = criterion_smooth.cuda()
    all_parameters = model.parameters()
    weight_parameters = []
    for (pname, p) in model.named_parameters():
        if (('fc' in pname) or ('conv1' in pname) or ('pwconv' in pname)):
            weight_parameters.append(p)
    weight_parameters_id = list(map(id, weight_parameters))
    other_parameters = list(filter((lambda p: (id(p) not in weight_parameters_id)), all_parameters))
    optimizer = torch.optim.SGD([{'params': other_parameters}, {'params': weight_parameters, 'weight_decay': args.weight_decay}], args.learning_rate, momentum=args.momentum)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, (lambda step: (1.0 - (step / args.epochs))), last_epoch=(- 1))
    start_epoch = 0
    best_top1_acc = 0
    checkpoint_tar = os.path.join(args.save, 'checkpoint.pth.tar')
    if os.path.exists(checkpoint_tar):
        logging.info('loading checkpoint {} ..........'.format(checkpoint_tar))
        checkpoint = torch.load(checkpoint_tar)
        start_epoch = checkpoint['epoch']
        best_top1_acc = checkpoint['best_top1_acc']
        model.load_state_dict(checkpoint['state_dict'])
        logging.info('loaded checkpoint {} epoch = {}'.format(checkpoint_tar, checkpoint['epoch']))
    for epoch in range(start_epoch):
        scheduler.step()
    traindir = os.path.join(args.data, 'train')
    valdir = os.path.join(args.data, 'val')
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    crop_scale = 0.08
    lighting_param = 0.1
    train_transforms = transforms.Compose([transforms.RandomResizedCrop(224, scale=(crop_scale, 1.0)), Lighting(lighting_param), transforms.RandomHorizontalFlip(), transforms.ToTensor(), normalize])
    train_dataset = datasets.ImageFolder(traindir, transform=train_transforms)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.workers, pin_memory=True)
    val_loader = torch.utils.data.DataLoader(datasets.ImageFolder(valdir, transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), normalize])), batch_size=args.batch_size, shuffle=False, num_workers=args.workers, pin_memory=True)
    epoch = start_epoch
    while (epoch < args.epochs):
        (train_obj, train_top1_acc, train_top5_acc, epoch) = train(epoch, train_loader, model, criterion_smooth, optimizer, scheduler)
        (valid_obj, valid_top1_acc, valid_top5_acc) = validate(epoch, val_loader, model, criterion, args)
        is_best = False
        if (valid_top1_acc > best_top1_acc):
            best_top1_acc = valid_top1_acc
            is_best = True
        save_checkpoint({'epoch': epoch, 'state_dict': model.state_dict(), 'best_top1_acc': best_top1_acc, 'optimizer': optimizer.state_dict()}, is_best, args.save)
        epoch += 1
    training_time = ((time.time() - start_t) / 36000)
    print('total training time = {} hours'.format(training_time))
