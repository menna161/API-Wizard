import os
import argparse
import numpy as np
from tqdm import tqdm
import pandas as pd
import joblib
from collections import OrderedDict
import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from utils import *
from wide_resnet import WideResNet
from auto_augment import AutoAugment, Cutout


def main():
    args = parse_args()
    if (args.name is None):
        args.name = ('%s_WideResNet%s-%s' % (args.dataset, args.depth, args.width))
        if args.cutout:
            args.name += '_wCutout'
        if args.auto_augment:
            args.name += '_wAutoAugment'
    if (not os.path.exists(('models/%s' % args.name))):
        os.makedirs(('models/%s' % args.name))
    print('Config -----')
    for arg in vars(args):
        print(('%s: %s' % (arg, getattr(args, arg))))
    print('------------')
    with open(('models/%s/args.txt' % args.name), 'w') as f:
        for arg in vars(args):
            print(('%s: %s' % (arg, getattr(args, arg))), file=f)
    joblib.dump(args, ('models/%s/args.pkl' % args.name))
    criterion = nn.CrossEntropyLoss().cuda()
    cudnn.benchmark = True
    if (args.dataset == 'cifar10'):
        transform_train = [transforms.RandomCrop(32, padding=4), transforms.RandomHorizontalFlip()]
        if args.auto_augment:
            transform_train.append(AutoAugment())
        if args.cutout:
            transform_train.append(Cutout())
        transform_train.extend([transforms.ToTensor(), transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.201))])
        transform_train = transforms.Compose(transform_train)
        transform_test = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5071, 0.4867, 0.4408), (0.2675, 0.2565, 0.2761))])
        train_set = datasets.CIFAR10(root='~/data', train=True, download=True, transform=transform_train)
        train_loader = torch.utils.data.DataLoader(train_set, batch_size=128, shuffle=True, num_workers=8)
        test_set = datasets.CIFAR10(root='~/data', train=False, download=True, transform=transform_test)
        test_loader = torch.utils.data.DataLoader(test_set, batch_size=128, shuffle=False, num_workers=8)
        num_classes = 10
    elif (args.dataset == 'cifar100'):
        transform_train = [transforms.RandomCrop(32, padding=4), transforms.RandomHorizontalFlip()]
        if args.auto_augment:
            transform_train.append(AutoAugment())
        if args.cutout:
            transform_train.append(Cutout())
        transform_train.extend([transforms.ToTensor(), transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.201))])
        transform_train = transforms.Compose(transform_train)
        transform_test = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.201))])
        train_set = datasets.CIFAR100(root='~/data', train=True, download=True, transform=transform_train)
        train_loader = torch.utils.data.DataLoader(train_set, batch_size=128, shuffle=True, num_workers=8)
        test_set = datasets.CIFAR100(root='~/data', train=False, download=True, transform=transform_test)
        test_loader = torch.utils.data.DataLoader(test_set, batch_size=128, shuffle=False, num_workers=8)
        num_classes = 100
    model = WideResNet(args.depth, args.width, num_classes=num_classes)
    model = model.cuda()
    optimizer = optim.SGD(filter((lambda p: p.requires_grad), model.parameters()), lr=args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
    scheduler = lr_scheduler.MultiStepLR(optimizer, milestones=[int(e) for e in args.milestones.split(',')], gamma=args.gamma)
    log = pd.DataFrame(index=[], columns=['epoch', 'lr', 'loss', 'acc', 'val_loss', 'val_acc'])
    best_acc = 0
    for epoch in range(args.epochs):
        print(('Epoch [%d/%d]' % ((epoch + 1), args.epochs)))
        scheduler.step()
        train_log = train(args, train_loader, model, criterion, optimizer, epoch)
        val_log = validate(args, test_loader, model, criterion)
        print(('loss %.4f - acc %.4f - val_loss %.4f - val_acc %.4f' % (train_log['loss'], train_log['acc'], val_log['loss'], val_log['acc'])))
        tmp = pd.Series([epoch, scheduler.get_lr()[0], train_log['loss'], train_log['acc'], val_log['loss'], val_log['acc']], index=['epoch', 'lr', 'loss', 'acc', 'val_loss', 'val_acc'])
        log = log.append(tmp, ignore_index=True)
        log.to_csv(('models/%s/log.csv' % args.name), index=False)
        if (val_log['acc'] > best_acc):
            torch.save(model.state_dict(), ('models/%s/model.pth' % args.name))
            best_acc = val_log['acc']
            print('=> saved best model')
