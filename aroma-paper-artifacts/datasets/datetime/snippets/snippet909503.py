import sys
import torch
import torch.nn as nn
import copy
import numpy as np
import random
import os
import experiments.cifar10.models as models
import experiments.cifar10.parser as parser
import experiments.cifar10.dataset as dataset
import experiments.cifar10.trainer as trainer
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
    if ('allcnnc' in args.model):
        args.epochs = 350
        args.batch_size = 128
        args.optim = 'sgd'
        args.weight_decay = 0.001
        assert (args.lr in [0.01, 0.05, 0.1, 0.25]), "lr:({}) not used in the 'AllCNNC' baseline. Must be one of [0.01, 0.05, 0.1, 0.25].".format(args.lr)
        model = models.AllCNNC()
        if (args.model == 'p4_allcnnc'):
            model = models.P4AllCNNC()
        if (args.model == 'f_att_p4_allcnnc'):
            model = models.fA_P4AllCNNC()
        if (args.model == 'p4m_allcnnc'):
            model = models.P4MAllCNNC()
        if (args.model == 'f_att_p4m_allcnnc'):
            model = models.fA_P4MAllCNNC()
    if ('resnet44' in args.model):
        args.epochs = 300
        args.batch_size = 128
        args.lr = 0.05
        args.optim = 'sgd'
        args.weight_decay = 0.0
        model = models.ResNet()
        if (args.model == 'p4m_resnet44'):
            model = models.P4MResNet()
        if (args.model == 'f_att_p4m_resnet44'):
            model = models.fA_P4MResNet()
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
        trainer.train(model, dataloaders, args)
    if args.pretrained:
        model.load_state_dict(torch.load(args.path))
    test(model, test_loader, args.device)
