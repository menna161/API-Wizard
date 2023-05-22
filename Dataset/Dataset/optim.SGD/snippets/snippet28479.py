import os
import random
import time
import cv2
import numpy as np
import logging
import argparse
import shutil
import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.nn.parallel
import torch.optim
import torch.utils.data
import torchvision
import torchvision.transforms as transforms
import torch.optim.lr_scheduler as lr_scheduler
import torch.multiprocessing as mp
import torch.distributed as dist
from tensorboardX import SummaryWriter
from model.san import san
from util import config
from util.util import AverageMeter, intersectionAndUnionGPU, find_free_port, mixup_data, mixup_loss, smooth_loss, cal_accuracy


def main_worker(gpu, ngpus_per_node, argss):
    global args, best_acc1
    (args, best_acc1) = (argss, 0)
    if args.distributed:
        if ((args.dist_url == 'env://') and (args.rank == (- 1))):
            args.rank = int(os.environ['RANK'])
        if args.multiprocessing_distributed:
            args.rank = ((args.rank * ngpus_per_node) + gpu)
        dist.init_process_group(backend=args.dist_backend, init_method=args.dist_url, world_size=args.world_size, rank=args.rank)
    model = san(args.sa_type, args.layers, args.kernels, args.classes)
    criterion = nn.CrossEntropyLoss(ignore_index=args.ignore_label)
    optimizer = torch.optim.SGD(model.parameters(), lr=args.base_lr, momentum=args.momentum, weight_decay=args.weight_decay)
    if (args.scheduler == 'step'):
        scheduler = lr_scheduler.MultiStepLR(optimizer, milestones=args.step_epochs, gamma=0.1)
    elif (args.scheduler == 'cosine'):
        scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    if main_process():
        global logger, writer
        logger = get_logger()
        writer = SummaryWriter(args.save_path)
        logger.info(args)
        logger.info('=> creating model ...')
        logger.info('Classes: {}'.format(args.classes))
        logger.info(model)
    if args.distributed:
        torch.cuda.set_device(gpu)
        args.batch_size = int((args.batch_size / ngpus_per_node))
        args.batch_size_val = int((args.batch_size_val / ngpus_per_node))
        args.workers = int((((args.workers + ngpus_per_node) - 1) / ngpus_per_node))
        model = torch.nn.parallel.DistributedDataParallel(model.cuda(), device_ids=[gpu])
    else:
        model = torch.nn.DataParallel(model.cuda())
    if args.weight:
        if os.path.isfile(args.weight):
            if main_process():
                logger.info("=> loading weight '{}'".format(args.weight))
            checkpoint = torch.load(args.weight)
            model.load_state_dict(checkpoint['state_dict'])
            if main_process():
                logger.info("=> loaded weight '{}'".format(args.weight))
        elif main_process():
            logger.info("=> no weight found at '{}'".format(args.weight))
    if args.resume:
        if os.path.isfile(args.resume):
            if main_process():
                logger.info("=> loading checkpoint '{}'".format(args.resume))
            checkpoint = torch.load(args.resume, map_location=(lambda storage, loc: storage.cuda(gpu)))
            args.start_epoch = checkpoint['epoch']
            best_acc1 = checkpoint['top1_val']
            model.load_state_dict(checkpoint['state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer'])
            scheduler.load_state_dict(checkpoint['scheduler'])
            if main_process():
                logger.info("=> loaded checkpoint '{}' (epoch {})".format(args.resume, checkpoint['epoch']))
        elif main_process():
            logger.info("=> no checkpoint found at '{}'".format(args.resume))
    (mean, std) = ([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    train_transform = transforms.Compose([transforms.RandomResizedCrop(224), transforms.RandomHorizontalFlip(), transforms.ToTensor(), transforms.Normalize(mean, std)])
    train_set = torchvision.datasets.ImageFolder(os.path.join(args.data_root, 'train'), train_transform)
    val_transform = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), transforms.Normalize(mean, std)])
    val_set = torchvision.datasets.ImageFolder(os.path.join(args.data_root, 'val'), val_transform)
    if args.distributed:
        train_sampler = torch.utils.data.distributed.DistributedSampler(train_set)
        val_sampler = torch.utils.data.distributed.DistributedSampler(val_set)
    else:
        train_sampler = None
        val_sampler = None
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=args.batch_size, shuffle=(train_sampler is None), num_workers=args.workers, pin_memory=True, sampler=train_sampler)
    val_loader = torch.utils.data.DataLoader(val_set, batch_size=args.batch_size_val, shuffle=False, num_workers=args.workers, pin_memory=True, sampler=val_sampler)
    for epoch in range(args.start_epoch, args.epochs):
        if args.distributed:
            train_sampler.set_epoch(epoch)
        (loss_train, mIoU_train, mAcc_train, allAcc_train, top1_train, top5_train) = train(train_loader, model, criterion, optimizer, epoch)
        (loss_val, mIoU_val, mAcc_val, allAcc_val, top1_val, top5_val) = validate(val_loader, model, criterion)
        scheduler.step()
        epoch_log = (epoch + 1)
        if main_process():
            writer.add_scalar('loss_train', loss_train, epoch_log)
            writer.add_scalar('mIoU_train', mIoU_train, epoch_log)
            writer.add_scalar('mAcc_train', mAcc_train, epoch_log)
            writer.add_scalar('allAcc_train', allAcc_train, epoch_log)
            writer.add_scalar('top1_train', top1_train, epoch_log)
            writer.add_scalar('top5_train', top5_train, epoch_log)
            writer.add_scalar('loss_val', loss_val, epoch_log)
            writer.add_scalar('mIoU_val', mIoU_val, epoch_log)
            writer.add_scalar('mAcc_val', mAcc_val, epoch_log)
            writer.add_scalar('allAcc_val', allAcc_val, epoch_log)
            writer.add_scalar('top1_val', top1_val, epoch_log)
            writer.add_scalar('top5_val', top5_val, epoch_log)
        if (((epoch_log % args.save_freq) == 0) and main_process()):
            filename = (((args.save_path + '/train_epoch_') + str(epoch_log)) + '.pth')
            logger.info(('Saving checkpoint to: ' + filename))
            torch.save({'epoch': epoch_log, 'state_dict': model.state_dict(), 'optimizer': optimizer.state_dict(), 'scheduler': scheduler.state_dict(), 'top1_val': top1_val, 'top5_val': top5_val}, filename)
            if (top1_val > best_acc1):
                best_acc1 = top1_val
                shutil.copyfile(filename, (args.save_path + '/model_best.pth'))
            if ((epoch_log / args.save_freq) > 2):
                deletename = (((args.save_path + '/train_epoch_') + str((epoch_log - (args.save_freq * 2)))) + '.pth')
                os.remove(deletename)
