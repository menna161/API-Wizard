import sys
import torch
import torch.nn as nn
import copy
import numpy as np
import random
import os
import experiments.pcam.models as models
import experiments.pcam.parser as parser
import experiments.pcam.dataset as dataset
import experiments.pcam.trainer as trainer, test
from experiments.logger import Logger
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import datetime


def main(args):
    args = copy.deepcopy(args)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)
    torch.backends.cudnn.benchmark = True
    if ('densenet' in args.model):
        args.epochs = 100
        args.weight_decay = 0.0001
        args.optim = 'adam'
        args.batch_size = 64
        args.lr = 0.001
        model = models.DenseNet(n_channels=26)
        if (args.model == 'p4_densenet'):
            model = models.P4DenseNet(n_channels=13)
        elif (args.model == 'f_att_p4_densenet'):
            model = models.fA_P4DenseNet(n_channels=13)
        elif (args.model == 'p4m_densenet'):
            model = models.P4MDenseNet(n_channels=9)
        elif (args.model == 'f_att_p4m_densenet'):
            model = models.P4MDenseNet(n_channels=9)
    args.device = ('cuda:0' if ((args.device == 'cuda') and torch.cuda.is_available()) else 'cpu')
    if (torch.cuda.device_count() > 1):
        print("Let's use", torch.cuda.device_count(), 'GPUs!')
    model = nn.DataParallel(model)
    model.to(args.device)
    (dataloaders, test_loader) = dataset.get_dataset(batch_size=args.batch_size, augmentation=args.augment, num_workers=4)
    model_directory(args)
    if (not args.pretrained):
        print(args)
        import datetime
        print(datetime.datetime.now())
        trainer.train(model, dataloaders, test_loader, args)
    if args.pretrained:
        model.load_state_dict(torch.load(args.path))
    trainer.test(model, test_loader, args.device)
