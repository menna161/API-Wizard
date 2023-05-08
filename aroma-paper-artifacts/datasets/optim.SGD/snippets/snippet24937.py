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
from math import cos, pi


def main():
    global args, best_prec1
    args = parser.parse_args()
    model_weight = torch.load('/opt/luojh/pretrained_models/ResNet50_ImageNet.pth')
    model = resnet50(model_weight, num_classes=args.class_num)
    model.eval()
    summary(model, torch.zeros((1, 3, 224, 224)))
    model = torch.nn.DataParallel(model.cuda(), device_ids=range(torch.cuda.device_count()))
    cudnn.benchmark = True
    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = torch.optim.SGD(filter((lambda p: p.requires_grad), model.parameters()), args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
    data_transforms = {'train': transforms.Compose([transforms.RandomResizedCrop(224), transforms.RandomHorizontalFlip(), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]), 'val': transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])}
    data_dir = args.data_base
    print('| Preparing model...')
    dsets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in ['train', 'val']}
    train_loader = torch.utils.data.DataLoader(dsets['train'], batch_size=args.batch_size, shuffle=True, num_workers=8, pin_memory=True)
    val_loader = torch.utils.data.DataLoader(dsets['val'], batch_size=args.batch_size, shuffle=False, num_workers=8, pin_memory=True)
    print('data_loader_success!')
    for epoch in range(args.start_epoch, args.epochs):
        train(train_loader, model, criterion, optimizer, epoch)
        prec1 = validate(val_loader, model, criterion)
        best_prec1 = max(prec1, best_prec1)
        folder_path = 'checkpoint/fine_tune'
        if (not os.path.exists(folder_path)):
            os.makedirs(folder_path)
        torch.save(model.state_dict(), (folder_path + '/model.pth'))
        print(('best acc is %.3f' % best_prec1))
