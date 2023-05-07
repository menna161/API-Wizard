import multiprocessing as mp
import argparse
import os
import time
import yaml
import pickle
import numpy
import logging
from easydict import EasyDict
from datetime import datetime
import pprint
from tensorboardX import SummaryWriter
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torch.optim
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import albumentations
from albumentations.augmentations.transforms import ShiftScaleRotate, HorizontalFlip, Normalize, RandomBrightnessContrast, MotionBlur, Blur, GaussNoise, JpegCompression, Resize, RandomBrightness, RandomResizedCrop
from albumentations.pytorch.transforms import ToTensorV2
import math
import torch.distributed as dist
from models import model_entry
from scheduler import get_scheduler
from dataset import FaceDataset
from utils import create_logger, AverageMeter, accuracy, save_checkpoint, load_state, DistributedGivenIterationSampler, DistributedSampler, parameters_string
from distributed_utils import dist_init
from optim import optim_entry


def main():
    global args, config, best_loss
    args = parser.parse_args()
    with open(args.config) as f:
        config = yaml.load(f)
    for (k, v) in config['common'].items():
        setattr(args, k, v)
    config = EasyDict(config['common'])
    (rank, world_size, device_id) = dist_init(os.path.join(args.distributed_path, config.distributed_file))
    args.save_path_dated = ((args.save_path + '/') + args.datetime)
    if (args.run_tag != ''):
        args.save_path_dated += ('-' + args.run_tag)
    model = model_entry(config.model)
    model.cuda()
    model = nn.parallel.DistributedDataParallel(model, device_ids=[device_id])
    opt_config = config.optimizer
    opt_config.kwargs.lr = config.lr_scheduler.base_lr
    opt_config.kwargs.params = model.parameters()
    optimizer = optim_entry(opt_config)
    last_iter = (- 1)
    best_loss = 1000000000.0
    if args.load_path:
        if args.recover:
            (best_loss, last_iter) = load_state(args.load_path, model, optimizer=optimizer)
        else:
            load_state(args.load_path, model)
    cudnn.benchmark = True
    if config.augmentation.get('imgnet_mean', False):
        model_mean = (0.485, 0.456, 0.406)
        model_std = (0.229, 0.224, 0.225)
    else:
        model_mean = (0.5, 0.5, 0.5)
        model_std = (0.5, 0.5, 0.5)
    trans = albumentations.Compose([RandomResizedCrop(config.augmentation.input_size, config.augmentation.input_size, scale=((config.augmentation.min_scale ** 2.0), 1.0), ratio=(1.0, 1.0)), HorizontalFlip(p=0.5), RandomBrightnessContrast(brightness_limit=0.25, contrast_limit=0.1, p=0.5), JpegCompression(p=0.2, quality_lower=50), MotionBlur(p=0.5), Normalize(mean=model_mean, std=model_std), ToTensorV2()])
    train_dataset = FaceDataset(config.train_root, config.train_source, transform=trans, resize=config.augmentation.input_size, image_format=config.get('image_format', None), random_frame=config.get('train_random_frame', False), bgr=config.augmentation.get('bgr', False))
    train_sampler = DistributedGivenIterationSampler(train_dataset, config.lr_scheduler.max_iter, config.batch_size, last_iter=last_iter)
    train_loader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=False, num_workers=config.workers, pin_memory=True, sampler=train_sampler)
    trans = albumentations.Compose([Resize(config.augmentation.input_size, config.augmentation.input_size), Normalize(mean=model_mean, std=model_std), ToTensorV2()])
    val_multi_loader = []
    if (args.val_source != ''):
        for dataset_idx in range(len(args.val_source)):
            val_dataset = FaceDataset(args.val_root[dataset_idx], args.val_source[dataset_idx], transform=trans, output_index=True, resize=config.augmentation.input_size, image_format=config.get('image_format', None), bgr=config.augmentation.get('bgr', False))
            val_sampler = DistributedSampler(val_dataset, round_up=False)
            val_loader = DataLoader(val_dataset, batch_size=config.batch_size, shuffle=False, num_workers=config.workers, pin_memory=True, sampler=val_sampler)
            val_multi_loader.append(val_loader)
    config.lr_scheduler['optimizer'] = optimizer
    config.lr_scheduler['last_iter'] = last_iter
    lr_scheduler = get_scheduler(config.lr_scheduler)
    if (rank == 0):
        mkdir(args.save_path)
        mkdir(args.save_path_dated)
        tb_logger = SummaryWriter(args.save_path_dated)
        logger = create_logger('global_logger', (args.save_path_dated + '-log.txt'))
        logger.info('{}'.format(args))
        logger.info(model)
        logger.info(parameters_string(model))
        logger.info(('len(train dataset) = %d' % len(train_loader.dataset)))
        for dataset_idx in range(len(val_multi_loader)):
            logger.info(('len(val%d dataset) = %d' % (dataset_idx, len(val_multi_loader[dataset_idx].dataset))))
        mkdir((args.save_path_dated + '/saves'))
    else:
        tb_logger = None
    positive_weight = config.get('positive_weight', 0.5)
    weight = (torch.tensor([(1.0 - positive_weight), positive_weight]) * 2.0)
    if (rank == 0):
        logger.info('using class weights: {}'.format(weight.tolist()))
    criterion = nn.CrossEntropyLoss(weight=weight).cuda()
    if args.evaluate:
        if args.evaluate_path:
            all_ckpt = get_all_checkpoint(args.evaluate_path, args.range_list, rank)
            for ckpt in all_ckpt:
                if (rank == 0):
                    logger.info(('Testing ckpt: ' + ckpt))
                last_iter = (- 1)
                (_, last_iter) = load_state(ckpt, model, optimizer=optimizer)
                for dataset_idx in range(len(val_multi_loader)):
                    validate(dataset_idx, val_multi_loader[dataset_idx], model, criterion, tb_logger, curr_step=last_iter, save_softmax=True)
        else:
            for dataset_idx in range(len(val_multi_loader)):
                validate(dataset_idx, val_multi_loader[dataset_idx], model, criterion, tb_logger, curr_step=last_iter, save_softmax=True)
        return
    train(train_loader, val_multi_loader, model, criterion, optimizer, lr_scheduler, (last_iter + 1), tb_logger)
    return
