from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import _init_paths
import os
import sys
import numpy as np
import argparse
import pprint
import pdb
import time
import logging
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
from datetime import datetime
import torchvision.transforms as transforms
from torch.utils.data.sampler import Sampler
from roi_data_layer.roidb import combined_roidb
from roi_data_layer.roibatchLoader import roibatchLoader
from model.utils.config import cfg, cfg_from_file, cfg_from_list, get_output_dir
from model.utils.net_utils import weights_normal_init, save_net, load_net, adjust_learning_rate, save_checkpoint, clip_gradient
from model.fpn.resnet import resnet
import pdb

if (__name__ == '__main__'):
    args = parse_args()
    print('Called with args:')
    print(args)
    args.imdb_name = 'visdrone_2017_trainval'
    args.imdbval_name = 'visdrone_2017_test'
    args.set_cfgs = ['FPN_ANCHOR_SCALES', '[16, 32, 64, 128, 256]', 'FPN_FEAT_STRIDES', '[4, 8, 16, 32, 64]', 'ANCHOR_RATIOS', '[0.5, 1, 2]', 'MAX_NUM_GT_BOXES', '60']
    args.cfg_file = ('cfgs/{}_ls.yml'.format(args.net) if args.lscale else 'cfgs/{}.yml'.format(args.net))
    if (args.cfg_file is not None):
        cfg_from_file(args.cfg_file)
    if (args.set_cfgs is not None):
        cfg_from_list(args.set_cfgs)
    print('Using config:')
    pprint.pprint(cfg)
    logging.info(cfg)
    np.random.seed(cfg.RNG_SEED)
    if (torch.cuda.is_available() and (not args.cuda)):
        print('WARNING: You have a CUDA device, so you should probably run with --cuda')
    cfg.TRAIN.USE_FLIPPED = False
    cfg.USE_GPU_NMS = args.cuda
    (imdb, roidb, ratio_list, ratio_index) = combined_roidb(args.imdb_name)
    train_size = len(roidb)
    print('{:d} roidb entries'.format(len(roidb)))
    output_dir = ((((args.save_dir + '/') + args.net) + '/') + args.dataset)
    if (not os.path.exists(output_dir)):
        os.makedirs(output_dir)
    sampler_batch = sampler(train_size, args.batch_size)
    dataset = roibatchLoader(roidb, ratio_list, ratio_index, args.batch_size, imdb.num_classes, training=True)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=args.batch_size, sampler=sampler_batch, num_workers=args.num_workers)
    im_data = torch.FloatTensor(1)
    im_info = torch.FloatTensor(1)
    num_boxes = torch.LongTensor(1)
    gt_boxes = torch.FloatTensor(1)
    if args.cuda:
        im_data = im_data.cuda()
        im_info = im_info.cuda()
        num_boxes = num_boxes.cuda()
        gt_boxes = gt_boxes.cuda()
    im_data = Variable(im_data)
    im_info = Variable(im_info)
    num_boxes = Variable(num_boxes)
    gt_boxes = Variable(gt_boxes)
    if args.cuda:
        cfg.CUDA = True
    if (args.net == 'res101'):
        FPN = resnet(imdb.classes, 101, pretrained=True, class_agnostic=args.class_agnostic)
    elif (args.net == 'res50'):
        FPN = resnet(imdb.classes, 50, pretrained=True, class_agnostic=args.class_agnostic)
    elif (args.net == 'res152'):
        FPN = resnet(imdb.classes, 152, pretrained=True, class_agnostic=args.class_agnostic)
    else:
        print('network is not defined')
        pdb.set_trace()
    FPN.create_architecture()
    lr = cfg.TRAIN.LEARNING_RATE
    lr = args.lr
    params = []
    for (key, value) in dict(FPN.named_parameters()).items():
        if value.requires_grad:
            if ('bias' in key):
                params += [{'params': [value], 'lr': (lr * (cfg.TRAIN.DOUBLE_BIAS + 1)), 'weight_decay': ((cfg.TRAIN.BIAS_DECAY and cfg.TRAIN.WEIGHT_DECAY) or 0)}]
            else:
                params += [{'params': [value], 'lr': lr, 'weight_decay': cfg.TRAIN.WEIGHT_DECAY}]
    if (args.optimizer == 'adam'):
        lr = (lr * 0.1)
        optimizer = torch.optim.Adam(params)
    elif (args.optimizer == 'sgd'):
        optimizer = torch.optim.SGD(params, momentum=cfg.TRAIN.MOMENTUM)
    load_name = os.path.join('models', 'baseline', 'fpn_{}_{}_{}.pth'.format(args.checksession, '1', '10161'))
    print(('loading checkpoint %s' % load_name))
    checkpoint = torch.load(load_name)
    for key in checkpoint['model'].keys():
        if any(((name in key) for name in ['RCNN_angle_score', 'RCNN_altitude_score', 'RCNN_weather_score', 'RCNN_angle', 'RCNN_weather', 'RCNN_altitude'])):
            del checkpoint['model'][key]
    model_dict = FPN.state_dict()
    model_dict.update(checkpoint['model'])
    FPN.load_state_dict(model_dict)
    print(('loaded checkpoint %s' % load_name))
    if args.mGPUs:
        FPN = nn.DataParallel(FPN)
    if args.cuda:
        FPN.cuda()
    iters_per_epoch = int((train_size / args.batch_size))
    for epoch in range(args.start_epoch, args.max_epochs):
        FPN.train()
        loss_temp = 0
        start = time.time()
        if ((epoch % (args.lr_decay_step + 1)) == 0):
            adjust_learning_rate(optimizer, args.lr_decay_gamma)
            lr *= args.lr_decay_gamma
        data_iter = iter(dataloader)
        for step in range(iters_per_epoch):
            data = data_iter.next()
            im_data.data.resize_(data[0].size()).copy_(data[0])
            im_info.data.resize_(data[1].size()).copy_(data[1])
            gt_boxes.data.resize_(data[2].size()).copy_(data[2])
            num_boxes.data.resize_(data[3].size()).copy_(data[3])
            FPN.zero_grad()
            (_, _, _, rpn_loss_cls, rpn_loss_box, RCNN_loss_cls, RCNN_loss_bbox, roi_labels) = FPN(im_data, im_info, gt_boxes, num_boxes)
            loss = (((rpn_loss_cls.mean() + rpn_loss_box.mean()) + RCNN_loss_cls.mean()) + RCNN_loss_bbox.mean())
            loss_temp += loss.item()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if ((step % args.disp_interval) == 0):
                end = time.time()
                if (step > 0):
                    loss_temp /= args.disp_interval
                if args.mGPUs:
                    loss_rpn_cls = rpn_loss_cls.mean().item()
                    loss_rpn_box = rpn_loss_box.mean().item()
                    loss_rcnn_cls = RCNN_loss_cls.mean().item()
                    loss_rcnn_box = RCNN_loss_bbox.mean().item()
                    fg_cnt = torch.sum(roi_labels.data.ne(0))
                    bg_cnt = (roi_labels.data.numel() - fg_cnt)
                else:
                    loss_rpn_cls = rpn_loss_cls.item()
                    loss_rpn_box = rpn_loss_box.item()
                    loss_rcnn_cls = RCNN_loss_cls.item()
                    loss_rcnn_box = RCNN_loss_bbox.item()
                    fg_cnt = torch.sum(roi_labels.data.ne(0))
                    bg_cnt = (roi_labels.data.numel() - fg_cnt)
                print(('[session %d][epoch %2d][iter %4d/%4d] loss: %.4f, lr: %.2e' % (args.session, epoch, step, iters_per_epoch, loss_temp, lr)))
                print(('\t\t\tfg/bg=(%d/%d), time cost: %f' % (fg_cnt, bg_cnt, (end - start))))
                print(('\t\t\trpn_cls: %.4f, rpn_box: %.4f, rcnn_cls: %.4f, rcnn_box %.4f' % (loss_rpn_cls, loss_rpn_box, loss_rcnn_cls, loss_rcnn_box)))
                loss_temp = 0
                start = time.time()
            if ((step % args.save_iters) == 0):
                save_name = os.path.join(args.save_dir, 'fpn_{}_{}_{}_adv.pth'.format(args.session, epoch, step))
                save_checkpoint({'session': args.session, 'epoch': epoch, 'model': (FPN.module.state_dict() if args.mGPUs else FPN.state_dict()), 'optimizer': optimizer.state_dict(), 'pooling_mode': cfg.POOLING_MODE, 'class_agnostic': args.class_agnostic}, save_name)
                print('save model: {}'.format(save_name))
        end = time.time()
        print((end - start))
