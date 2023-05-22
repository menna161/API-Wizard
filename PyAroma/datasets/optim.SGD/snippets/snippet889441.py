from __future__ import print_function
import argparse
import torch
import torch.nn.functional as F
import torch.optim as optim
import os
import math
import data_loader
import ResNet as models
from torch.utils import model_zoo

if (__name__ == '__main__'):
    model = models.MRANNet(num_classes=31)
    print(model)
    if args.cuda:
        model.cuda()
    (train_loader, unsuptrain_loader, test_loader) = load_data()
    correct = 0
    optimizer = torch.optim.SGD([{'params': model.sharedNet.parameters()}, {'params': model.Inception.parameters(), 'lr': args.lr[1]}], lr=args.lr[0], momentum=args.momentum, weight_decay=args.l2_decay)
    for epoch in range(1, (args.epochs + 1)):
        for (index, param_group) in enumerate(optimizer.param_groups):
            param_group['lr'] = (args.lr[index] / math.pow((1 + ((10 * (epoch - 1)) / args.epochs)), 0.75))
        train(epoch, model, train_loader, unsuptrain_loader, optimizer)
        t_correct = test(model, test_loader)
        if (t_correct > correct):
            correct = t_correct
        print(('%s max correct:' % args.test_dir), correct.item())
        print(args.source_dir, 'to', args.test_dir)
