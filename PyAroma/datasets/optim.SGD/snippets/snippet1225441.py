import argparse
import os
import shutil
import time
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
import numpy as np
from apex.parallel import DistributedDataParallel as DDP
from apex.fp16_utils import *
import apex


def main():
    global best_prec1, args
    args.distributed = False
    if ('WORLD_SIZE' in os.environ):
        args.distributed = (int(os.environ['WORLD_SIZE']) > 1)
    args.gpu = 0
    args.world_size = 1
    if args.distributed:
        args.gpu = (args.local_rank % torch.cuda.device_count())
        torch.cuda.set_device(args.gpu)
        torch.distributed.init_process_group(backend='nccl', init_method='env://')
        args.world_size = torch.distributed.get_world_size()
    if args.fp16:
        assert torch.backends.cudnn.enabled, 'fp16 mode requires cudnn backend to be enabled.'
    if (args.static_loss_scale != 1.0):
        if (not args.fp16):
            print('Warning:  if --fp16 is not used, static_loss_scale will be ignored.')
    if args.pretrained:
        print("=> using pre-trained model '{}'".format(args.arch))
        model = models.__dict__[args.arch](pretrained=True)
    else:
        print("=> creating model '{}'".format(args.arch))
        model = models.__dict__[args.arch]()
    if args.sync_bn:
        import apex
        print('using apex synced BN')
        model = apex.parallel.convert_syncbn_model(model)
    model = model.cuda()
    if args.fp16:
        model = network_to_half(model)
    if args.distributed:
        model = DDP(model, delay_allreduce=True)
    criterion = nn.CrossEntropyLoss().cuda()
    args.lr = ((args.lr * float((args.batch_size * args.world_size))) / 256.0)
    optimizer = torch.optim.SGD(model.parameters(), args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
    if args.fp16:
        optimizer = FP16_Optimizer(optimizer, static_loss_scale=args.static_loss_scale, dynamic_loss_scale=args.dynamic_loss_scale)
    if args.resume:

        def resume():
            if os.path.isfile(args.resume):
                print("=> loading checkpoint '{}'".format(args.resume))
                checkpoint = torch.load(args.resume, map_location=(lambda storage, loc: storage.cuda(args.gpu)))
                args.start_epoch = checkpoint['epoch']
                best_prec1 = checkpoint['best_prec1']
                model.load_state_dict(checkpoint['state_dict'])
                optimizer.load_state_dict(checkpoint['optimizer'])
                print("=> loaded checkpoint '{}' (epoch {})".format(args.resume, checkpoint['epoch']))
            else:
                print("=> no checkpoint found at '{}'".format(args.resume))
        resume()
    traindir = os.path.join(args.data, 'train')
    valdir = os.path.join(args.data, 'val')
    if (args.arch == 'inception_v3'):
        crop_size = 299
        val_size = 320
    else:
        crop_size = 224
        val_size = 256
    train_dataset = datasets.ImageFolder(traindir, transforms.Compose([transforms.RandomResizedCrop(crop_size), transforms.RandomHorizontalFlip()]))
    val_dataset = datasets.ImageFolder(valdir, transforms.Compose([transforms.Resize(val_size), transforms.CenterCrop(crop_size)]))
    train_sampler = None
    val_sampler = None
    if args.distributed:
        train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
        val_sampler = torch.utils.data.distributed.DistributedSampler(val_dataset)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=args.batch_size, shuffle=(train_sampler is None), num_workers=args.workers, pin_memory=True, sampler=train_sampler, collate_fn=fast_collate)
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=args.workers, pin_memory=True, sampler=val_sampler, collate_fn=fast_collate)
    if args.evaluate:
        validate(val_loader, model, criterion)
        return
    for epoch in range(args.start_epoch, args.epochs):
        if args.distributed:
            train_sampler.set_epoch(epoch)
        train(train_loader, model, criterion, optimizer, epoch)
        if args.prof:
            break
        prec1 = validate(val_loader, model, criterion)
        if (args.local_rank == 0):
            is_best = (prec1 > best_prec1)
            best_prec1 = max(prec1, best_prec1)
            save_checkpoint({'epoch': (epoch + 1), 'arch': args.arch, 'state_dict': model.state_dict(), 'best_prec1': best_prec1, 'optimizer': optimizer.state_dict()}, is_best)
