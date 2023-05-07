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
import torch.distributed as dist
import pprint
from tensorboardX import SummaryWriter
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import math
import torch.distributed as dist
from models import model_entry
from scheduler import get_scheduler
from dataset import VideoDataset
from mean import *
from spatial_transforms import *
from temporal_transforms import *
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
    if config.get('pretrain_path', None):
        load_state(config.pretrain_path, model)
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
    config.mean = get_mean(config.norm_value, dataset=config.mean_dataset)
    config.std = get_std(config.norm_value, dataset=config.mean_dataset)
    norm_method = Normalize(config.mean, config.std)
    opt = config.augmentation
    adjacent = config.model.kwargs.get('adjacent', 1)
    spatial_transform = [ScaleJitteringRandomCrop(opt.min_scale, opt.max_scale, opt.input_size), RandomHorizontalFlip()]
    if opt.get('brightnesscontrast', False):
        spatial_transform.append(RandomBrightnessContrast(brightness_limit=0.25, contrast_limit=0.1, p=0.5))
    if opt.get('jpegcompression', False):
        spatial_transform.append(ImageCompression(p=0.2, quality_lower=50))
    if opt.get('motionblur', False):
        spatial_transform.append(MotionBlur(p=0.5))
    spatial_transform = Compose((spatial_transform + [ToTensor(config.norm_value), norm_method]))
    train_aug_str = ', '.join([_.__class__.__name__ for _ in spatial_transform.transforms])
    if (opt.temporal_crop == 'random'):
        temporal_transform = TemporalRandomCrop(opt.sample_duration, opt.sample_step, adjacent)
    elif (opt.temporal_crop == 'center'):
        temporal_transform = TemporalCenterCrop(opt.sample_duration, opt.sample_step, adjacent)
    else:
        raise NotImplementedError(('Temporal crop type %s not supported!' % opt.temporal_crop))
    train_dataset = VideoDataset(config.train_root, config.train_source, spatial_transform, temporal_transform, image_format=config.get('image_format', None))
    train_sampler = DistributedGivenIterationSampler(train_dataset, config.lr_scheduler.max_iter, config.batch_size, last_iter=last_iter)
    train_loader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=False, num_workers=config.workers, pin_memory=True, sampler=train_sampler)
    spatial_transform = Compose([Scale(opt.val_input_size), ToTensor(config.norm_value), norm_method])
    val_aug_str = ', '.join([_.__class__.__name__ for _ in spatial_transform.transforms])
    if opt.get('val_no_temporal_crop', False):
        temporal_transform = TemporalSampling(opt.sample_step, adjacent)
        val_batch_size = 1
    else:
        temporal_transform = TemporalCenterCrop(opt.sample_duration, opt.sample_step, adjacent)
        val_batch_size = min(32, args.batch_size)
    val_multi_loader = []
    if (args.val_source != ''):
        for dataset_idx in range(len(args.val_source)):
            val_dataset = VideoDataset(args.val_root[dataset_idx], args.val_source[dataset_idx], spatial_transform, temporal_transform, output_index=True, image_format=config.get('image_format', None))
            val_sampler = DistributedSampler(val_dataset, round_up=True)
            val_loader = DataLoader(val_dataset, batch_size=val_batch_size, shuffle=False, num_workers=config.workers, pin_memory=True, sampler=val_sampler)
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
        logger.info(('train spatial augmentations: %s' % train_aug_str))
        for dataset_idx in range(len(val_multi_loader)):
            logger.info(('len(val%d dataset) = %d' % (dataset_idx, len(val_multi_loader[dataset_idx].dataset))))
        logger.info(('val spatial augmentations: %s' % val_aug_str))
        mkdir((args.save_path_dated + '/saves'))
    else:
        tb_logger = None
    positive_weight = config.get('positive_weight', 0.5)
    weight = (torch.tensor([(1.0 - positive_weight), positive_weight]) * 2.0)
    if (rank == 0):
        logger.info('using class weights: {}'.format(weight.tolist()))
    criterion = nn.CrossEntropyLoss(weight=weight).cuda()
    if args.evaluate:
        dist.barrier()
        print(('Rank %d saving to %s' % (rank, args.save_path_dated)))
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
