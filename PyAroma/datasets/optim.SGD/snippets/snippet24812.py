import argparse
import os
import shutil
import time
import sys
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
from torchvision import datasets, transforms
from torchsummaryX import summary
from pruned_model import resnet50
from ori_model import ori_resnet50
from math import cos, pi
import numpy as np
import yaml


def main():
    global args, best_prec1
    args = parser.parse_args()
    model_weight = torch.load(FLAGS['pretrain_model'])
    model = resnet50(model_weight, num_classes=FLAGS['class_num'])
    model.eval()
    summary(model, torch.zeros((1, 3, 224, 224)))
    model = model.cuda()
    cudnn.benchmark = True
    model_teacher = ori_resnet50(num_classes=FLAGS['class_num'])
    model_teacher = torch.nn.DataParallel(model_teacher.cuda(), device_ids=range(torch.cuda.device_count()))
    model_teacher.load_state_dict(model_weight)
    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = torch.optim.SGD(filter((lambda p: p.requires_grad), model.parameters()), args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
    data_transforms = {'train': transforms.Compose([transforms.RandomResizedCrop(224), transforms.RandomHorizontalFlip(), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]), 'val': transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])}
    data_dir = FLAGS['data_base']
    print('| Preparing model...')
    dsets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in ['train', 'val']}
    train_loader = torch.utils.data.DataLoader(dsets['train'], batch_size=FLAGS['batch_size'], shuffle=True, num_workers=8, pin_memory=True)
    val_loader = torch.utils.data.DataLoader(dsets['val'], batch_size=(4 * FLAGS['batch_size']), shuffle=False, num_workers=8, pin_memory=True)
    print('data_loader_success!')
    validate(val_loader, model, criterion)
    for epoch in range(args.start_epoch, args.epochs):
        train(train_loader, model_teacher, model, criterion, optimizer, epoch)
        prec1 = validate(val_loader, model, criterion)
        best_prec1 = max(prec1, best_prec1)
        folder_path = 'checkpoint/fine_tune'
        if (not os.path.exists(folder_path)):
            os.makedirs(folder_path)
        torch.save(model.state_dict(), (folder_path + '/model.pth'))
        print(('best acc is %.3f' % best_prec1))
