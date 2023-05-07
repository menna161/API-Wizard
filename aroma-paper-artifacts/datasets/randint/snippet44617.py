from __future__ import division, print_function
import sys
from copy import deepcopy
import math
import argparse
import torch
import torch.nn.init
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch.backends.cudnn as cudnn
import os
from tqdm import tqdm
import numpy as np
import random
import cv2
import copy
import PIL
from EvalMetrics import ErrorRateAt95Recall
from Losses import loss_HardNet, loss_random_sampling, loss_L2Net, global_orthogonal_regularization
from W1BS import w1bs_extract_descs_and_save
from Utils import L2Norm, cv2_scale, np_reshape
from Utils import str2bool
import torch.nn as nn
import torch.nn.functional as F
import utils.w1bs as w1bs
from Loggers import Logger, FileLogger


def main(train_loader, test_loaders, model, logger, file_logger):
    print('\nparsed options:\n{}\n'.format(vars(args)))
    if args.cuda:
        model.cuda()
    optimizer1 = create_optimizer(model.features, args.lr)
    if args.resume:
        if os.path.isfile(args.resume):
            print('=> loading checkpoint {}'.format(args.resume))
            checkpoint = torch.load(args.resume)
            args.start_epoch = checkpoint['epoch']
            checkpoint = torch.load(args.resume)
            model.load_state_dict(checkpoint['state_dict'])
        else:
            print('=> no checkpoint found at {}'.format(args.resume))
    start = args.start_epoch
    end = (start + args.epochs)
    for epoch in range(start, end):
        train(train_loader, model, optimizer1, epoch, logger, triplet_flag)
        if ((epoch % 5) == 4):
            for test_loader in test_loaders:
                test(test_loader['dataloader'], model, epoch, logger, test_loader['name'])
        '        \n        if TEST_ON_W1BS :\n            # print(weights_path)\n            patch_images = w1bs.get_list_of_patch_images(\n                DATASET_DIR=args.w1bsroot.replace(\'/code\', \'/data/W1BS\'))\n            desc_name = \'curr_desc\'# + str(random.randint(0,100))\n            \n            DESCS_DIR = LOG_DIR + \'/temp_descs/\' #args.w1bsroot.replace(\'/code\', "/data/out_descriptors")\n            OUT_DIR = DESCS_DIR.replace(\'/temp_descs/\', "/out_graphs/")\n\n            for img_fname in patch_images:\n                w1bs_extract_descs_and_save(img_fname, model, desc_name, cuda = args.cuda,\n                                            mean_img=args.mean_image,\n                                            std_img=args.std_image, out_dir = DESCS_DIR)\n\n\n            force_rewrite_list = [desc_name]\n            w1bs.match_descriptors_and_save_results(DESC_DIR=DESCS_DIR, do_rewrite=True,\n                                                    dist_dict={},\n                                                    force_rewrite_list=force_rewrite_list)\n            if(args.enable_logging):\n                w1bs.draw_and_save_plots_with_loggers(DESC_DIR=DESCS_DIR, OUT_DIR=OUT_DIR,\n                                         methods=["SNN_ratio"],\n                                         descs_to_draw=[desc_name],\n                                         logger=file_logger,\n                                         tensor_logger = logger)\n            else:\n                w1bs.draw_and_save_plots(DESC_DIR=DESCS_DIR, OUT_DIR=OUT_DIR,\n                                         methods=["SNN_ratio"],\n                                         descs_to_draw=[desc_name])\n        #randomize train loader batches\n\n        train_loader, test_loaders2 = create_loaders(load_random_triplets=triplet_flag)\n        '
        print('i am here')
