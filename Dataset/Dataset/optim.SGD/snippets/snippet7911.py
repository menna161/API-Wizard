import sys
import os
import argparse
import random
import shutil
import time
import warnings
from apex import amp
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
from thop import profile
from thop import clever_format
from torch.utils.data import DataLoader
from config import Config
from densenet import densenet161
from public.imagenet.utils import DataPrefetcher, get_logger, AverageMeter, accuracy


def main(logger, args):
    if (not torch.cuda.is_available()):
        raise Exception('need gpu to train network!')
    if (args.seed is not None):
        random.seed(args.seed)
        torch.cuda.manual_seed_all(args.seed)
        cudnn.deterministic = True
    gpus = torch.cuda.device_count()
    logger.info(f'use {gpus} gpus')
    logger.info(f'args: {args}')
    cudnn.benchmark = True
    cudnn.enabled = True
    start_time = time.time()
    logger.info('start loading data')
    train_loader = DataLoader(Config.train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.num_workers)
    val_loader = DataLoader(Config.val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers)
    logger.info('finish loading data')
    logger.info(f"creating model '{args.network}'")
    model = densenet161(**{'pretrained': args.pretrained, 'num_classes': args.num_classes})
    flops_input = torch.randn(1, 3, args.input_image_size, args.input_image_size)
    (flops, params) = profile(model, inputs=(flops_input,))
    (flops, params) = clever_format([flops, params], '%.3f')
    logger.info(f"model: '{args.network}', flops: {flops}, params: {params}")
    for (name, param) in model.named_parameters():
        logger.info(f'{name},{param.requires_grad}')
    model = model.cuda()
    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = torch.optim.SGD(model.parameters(), args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=args.milestones, gamma=0.1)
    if args.apex:
        (model, optimizer) = amp.initialize(model, optimizer, opt_level='O1')
    model = nn.DataParallel(model)
    if args.evaluate:
        if (not os.path.isfile(args.evaluate)):
            raise Exception(f'{args.resume} is not a file, please check it again')
        logger.info('start only evaluating')
        logger.info(f'start resuming model from {args.evaluate}')
        checkpoint = torch.load(args.evaluate, map_location=torch.device('cpu'))
        model.load_state_dict(checkpoint['model_state_dict'])
        (acc1, acc5, throughput) = validate(val_loader, model, args)
        logger.info(f"epoch {checkpoint['epoch']:0>3d}, top1 acc: {acc1:.2f}%, top5 acc: {acc5:.2f}%, throughput: {throughput:.2f}sample/s")
        return
    start_epoch = 1
    if os.path.exists(args.resume):
        logger.info(f'start resuming model from {args.resume}')
        checkpoint = torch.load(args.resume, map_location=torch.device('cpu'))
        start_epoch += checkpoint['epoch']
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        logger.info(f"finish resuming model from {args.resume}, epoch {checkpoint['epoch']}, loss: {checkpoint['loss']:3f}, lr: {checkpoint['lr']:.6f}, top1_acc: {checkpoint['acc1']}%")
    if (not os.path.exists(args.checkpoints)):
        os.makedirs(args.checkpoints)
    logger.info('start training')
    for epoch in range(start_epoch, (args.epochs + 1)):
        (acc1, acc5, losses) = train(train_loader, model, criterion, optimizer, scheduler, epoch, logger, args)
        logger.info(f'train: epoch {epoch:0>3d}, top1 acc: {acc1:.2f}%, top5 acc: {acc5:.2f}%, losses: {losses:.2f}')
        (acc1, acc5, throughput) = validate(val_loader, model, args)
        logger.info(f'val: epoch {epoch:0>3d}, top1 acc: {acc1:.2f}%, top5 acc: {acc5:.2f}%, throughput: {throughput:.2f}sample/s')
        torch.save({'epoch': epoch, 'acc1': acc1, 'loss': losses, 'lr': scheduler.get_lr()[0], 'model_state_dict': model.state_dict(), 'optimizer_state_dict': optimizer.state_dict(), 'scheduler_state_dict': scheduler.state_dict()}, os.path.join(args.checkpoints, 'latest.pth'))
        if (epoch == args.epochs):
            torch.save(model.module.state_dict(), os.path.join(args.checkpoints, '{}-epoch{}-acc{}.pth'.format(args.network, epoch, acc1)))
    training_time = ((time.time() - start_time) / 3600)
    logger.info(f'finish training, total training time: {training_time:.2f} hours')
