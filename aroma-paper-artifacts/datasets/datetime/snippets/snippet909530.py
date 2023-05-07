import sys
import torch
import torch.nn as nn
import copy
import numpy as np
import random
import os
import experiments.rot_mnist.models as models
import experiments.rot_mnist.parser as parser
import experiments.rot_mnist.dataset as dataset
import experiments.rot_mnist.trainer as trainer
from experiments.logger import Logger
import datetime


def main(args):
    args = copy.deepcopy(args)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)
    torch.backends.cudnn.benchmark = True
    args.weight_decay = 0.0001
    args.lr = 0.001
    args.optim = 'adam'
    args.batch_size = 128
    if (args.model == 'z2cnn'):
        model = models.Z2CNN()
        args.epochs = 300
    elif (args.model == 'p4cnn'):
        model = models.P4CNN()
        args.epochs = 100
    elif (args.model == 'att_p4cnn'):
        model = models.A_P4CNN()
        args.epochs = 100
    elif (args.model == 'sp_att_p4cnn'):
        model = models.A_Sp_P4CNN()
        args.epochs = 100
    elif (args.model == 'ch_att_p4cnn'):
        model = models.A_Ch_P4CNN()
        args.epochs = 100
    elif (args.model == 'f_att_p4cnn'):
        model = models.fA_P4CNN()
        args.epochs = 100
    elif (args.model == 'RomHog_att_p4cnn'):
        model = models.RomHog_fA_P4CNN()
        args.epochs = 100
    args.device = ('cuda:0' if ((args.device == 'cuda') and torch.cuda.is_available()) else 'cpu')
    model.to(args.device)
    (dataloaders, test_loader) = dataset.get_dataset(batch_size=args.batch_size, num_workers=4)
    model_directory(args)
    if (not args.pretrained):
        print(args)
        import datetime
        print(datetime.datetime.now())
        trainer.train(model, dataloaders, args)
    if args.pretrained:
        model.load_state_dict(torch.load(args.path))
    test(model, test_loader, args.device)
