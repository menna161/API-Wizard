import argparse
import os
import random
import shutil
import time
import warnings
import sys
import numpy as np
import os
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
import torch.multiprocessing as mp
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import models_lpf
import models_fconv_lpf
import torchvision.models as models
import resnet_fconv
import vgg_fconv
from IPython import embed
import matplotlib.pyplot as plt
import os
import models_lpf.resnet
import models_fconv_lpf.resnet
import models_lpf.vgg
import models_fconv_lpf.vgg


def main_worker(gpu, ngpus_per_node, args):
    global best_acc1
    args.gpu = gpu
    if (args.gpu is not None):
        print('Use GPU: {} for training'.format(args.gpu))
    if args.distributed:
        if ((args.dist_url == 'env://') and (args.rank == (- 1))):
            args.rank = int(os.environ['RANK'])
        if args.multiprocessing_distributed:
            args.rank = ((args.rank * ngpus_per_node) + gpu)
        dist.init_process_group(backend=args.dist_backend, init_method=args.dist_url, world_size=args.world_size, rank=args.rank)
    if args.pretrained:
        print("=> using pre-trained model '{}'".format(args.arch))
        model = models.__dict__[args.arch](pretrained=True)
    else:
        print("=> creating model '{}'".format(args.arch))
        import models_lpf.resnet
        import models_fconv_lpf.resnet
        import models_lpf.vgg
        import models_fconv_lpf.vgg
        if (args.arch == 'vgg11_bn_fconv'):
            model = vgg_fconv.vgg11_bn(num_classes=args.num_class)
        elif (args.arch == 'vgg13_bn_fconv'):
            model = vgg_fconv.vgg13_bn(num_classes=args.num_class)
        elif (args.arch == 'vgg16_bn_fconv'):
            model = vgg_fconv.vgg16_bn(num_classes=args.num_class)
        elif (args.arch == 'vgg19_bn_fconv'):
            model = vgg_fconv.vgg19_bn(num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg11_bn_lpf'):
            model = models_lpf.vgg11_bn(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg13_bn_lpf'):
            model = models_lpf.vgg.vgg13_bn(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg16_bn_lpf'):
            model = models_lpf.vgg.vgg16_bn(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg19_bn_lpf'):
            model = models_lpf.vgg.vgg19_bn(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg11_bn_fconv_lpf'):
            model = models_fconv_lpf.vgg.vgg11_bn(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg13_bn_fconv_lpf'):
            model = models_fconv_lpf.vgg.vgg13_bn(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg16_bn_fconv_lpf'):
            model = models_fconv_lpf.vgg.vgg16_bn(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg19_bn_fconv_lpf'):
            model = models_fconv_lpf.vgg.vgg19_bn(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch == 'vgg11_fconv'):
            model = vgg_fconv.vgg11(num_classes=args.num_class)
        elif (args.arch == 'vgg13_fconv'):
            model = vgg_fconv.vgg13(num_classes=args.num_class)
        elif (args.arch == 'vgg16_fconv'):
            model = vgg_fconv.vgg16(num_classes=args.num_class)
        elif (args.arch == 'vgg19_fconv'):
            model = vgg_fconv.vgg19(num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg11_lpf'):
            model = models_lpf.vgg.vgg11(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg13_lpf'):
            model = models_lpf.vgg.vgg13(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg16_lpf'):
            model = models_lpf.vgg.vgg16(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg19_lpf'):
            model = models_lpf.vgg.vgg19(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg11_fconv_lpf'):
            model = models_fconv_lpf.vgg.vgg11(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg13_fconv_lpf'):
            model = models_fconv_lpf.vgg.vgg13(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg16_fconv_lpf'):
            model = models_fconv_lpf.vgg.vgg16(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'vgg19_fconv_lpf'):
            model = models_fconv_lpf.vgg.vgg19(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch == 'resnet18_fconv'):
            model = resnet_fconv.resnet18(num_classes=args.num_class)
        elif (args.arch == 'resnet34_fconv'):
            model = resnet_fconv.resnet34(num_classes=args.num_class)
        elif (args.arch == 'resnet50_fconv'):
            model = resnet_fconv.resnet50(num_classes=args.num_class)
        elif (args.arch == 'resnet101_fconv'):
            model = resnet_fconv.resnet101(num_classes=args.num_class)
        elif (args.arch == 'resnet152_fconv'):
            model = resnet_fconv.resnet152(num_classes=args.num_class)
        elif (args.arch == 'resnext50_32x4d_fconv'):
            model = resnet_fconv.resnext50_32x4d(num_classes=args.num_class)
        elif (args.arch == 'resnext101_32x8d_fconv'):
            model = resnet_fconv.resnext101_32x8d(num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'resnet18_lpf'):
            model = models_lpf.resnet.resnet18(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'resnet34_lpf'):
            model = models_lpf.resnet.resnet34(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'resnet50_lpf'):
            model = models_lpf.resnet.resnet50(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'resnet101_lpf'):
            model = models_lpf.resnet.resnet101(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'resnet152_lpf'):
            model = models_lpf.resnet.resnet152(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'resnet18_fconv_lpf'):
            model = models_fconv_lpf.resnet.resnet18(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'resnet34_fconv_lpf'):
            model = models_fconv_lpf.resnet.resnet34(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'resnet50_fconv_lpf'):
            model = models_fconv_lpf.resnet.resnet50(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'resnet101_fconv_lpf'):
            model = models_fconv_lpf.resnet.resnet101(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        elif (args.arch[:(- 1)] == 'resnet152_fconv_lpf'):
            model = models_fconv_lpf.resnet.resnet152(filter_size=int(args.arch[(- 1)]), num_classes=args.num_class)
        else:
            model = models.__dict__[args.arch]()
    if (args.weights is not None):
        print(('=> using saved weights [%s]' % args.weights))
        weights = torch.load(args.weights)
        model.load_state_dict(weights['state_dict'])
    if args.distributed:
        if (args.gpu is not None):
            torch.cuda.set_device(args.gpu)
            model.cuda(args.gpu)
            args.batch_size = int((args.batch_size / ngpus_per_node))
            args.workers = int((args.workers / ngpus_per_node))
            model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.gpu])
        else:
            model.cuda()
            model = torch.nn.parallel.DistributedDataParallel(model)
    elif (args.gpu is not None):
        torch.cuda.set_device(args.gpu)
        model = model.cuda(args.gpu)
    elif (args.arch.startswith('alexnet') or args.arch.startswith('vgg')):
        model.features = torch.nn.DataParallel(model.features)
        model.cuda()
    else:
        model = torch.nn.DataParallel(model).cuda()
    criterion = nn.CrossEntropyLoss().cuda(args.gpu)
    optimizer = torch.optim.SGD(model.parameters(), args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
    if args.resume:
        if os.path.isfile(args.resume):
            print("=> loading checkpoint '{}'".format(args.resume))
            checkpoint = torch.load(args.resume)
            model.load_state_dict(checkpoint['state_dict'], strict=False)
            if ('optimizer' in checkpoint.keys()):
                args.start_epoch = checkpoint['epoch']
                best_acc1 = checkpoint['best_acc1']
                if (args.gpu is not None):
                    best_acc1 = best_acc1.to(args.gpu)
                optimizer.load_state_dict(checkpoint['optimizer'])
            else:
                print('  No optimizer saved')
            print("=> loaded checkpoint '{}' (epoch {})".format(args.resume, checkpoint['epoch']))
        else:
            print("=> no checkpoint found at '{}'".format(args.resume))
    cudnn.benchmark = True
    traindir = os.path.join(args.data, 'train')
    valdir = os.path.join(args.data, 'val')
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    normalize = transforms.Normalize(mean=mean, std=std)
    if args.no_data_aug:
        train_dataset = datasets.ImageFolder(traindir, transforms.Compose([transforms.Resize((256 + args.shift_inc)), transforms.CenterCrop(224), transforms.RandomHorizontalFlip(), transforms.ToTensor(), normalize]))
    else:
        train_dataset = datasets.ImageFolder(traindir, transforms.Compose([transforms.RandomResizedCrop(224), transforms.RandomHorizontalFlip(), transforms.ToTensor(), normalize]))
    if args.distributed:
        train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
    else:
        train_sampler = None
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=args.batch_size, shuffle=(train_sampler is None), num_workers=args.workers, pin_memory=True, sampler=train_sampler)
    crop_size = ((256 + args.shift_inc) if (args.evaluate_shift or args.evaluate_diagonal or args.evaluate_save) else 224)
    args.batch_size = (1 if (args.evaluate_diagonal or args.evaluate_save) else args.batch_size)
    val_loader = torch.utils.data.DataLoader(datasets.ImageFolder(valdir, transforms.Compose([transforms.Resize((256 + args.shift_inc)), transforms.CenterCrop(crop_size), transforms.ToTensor(), normalize])), batch_size=args.batch_size, shuffle=False, num_workers=args.workers, pin_memory=True)
    if args.val_debug:
        train_loader = val_loader
    if args.embed:
        embed()
    if (args.save_weights is not None):
        print(("=> saving 'deparallelized' weights [%s]" % args.save_weights))
        if (args.gpu is not None):
            torch.save({'state_dict': model.state_dict()}, args.save_weights)
        elif ((args.arch[:7] == 'alexnet') or (args.arch[:3] == 'vgg')):
            model.features = model.features.module
            torch.save({'state_dict': model.state_dict()}, args.save_weights)
        else:
            torch.save({'state_dict': model.module.state_dict()}, args.save_weights)
        return
    if args.evaluate:
        validate(val_loader, model, criterion, args)
        return
    if args.evaluate_shift:
        validate_shift(val_loader, model, args)
        return
    if args.evaluate_diagonal:
        validate_diagonal(val_loader, model, args)
        return
    if args.evaluate_save:
        validate_save(val_loader, mean, std, args)
        return
    if args.cos_lr:
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, args.epochs)
        for epoch in range(args.start_epoch):
            scheduler.step()
    for epoch in range(args.start_epoch, args.epochs):
        if args.distributed:
            train_sampler.set_epoch(epoch)
        if (not args.cos_lr):
            adjust_learning_rate(optimizer, epoch, args)
        else:
            scheduler.step()
            print(('[%03d] %.5f' % (epoch, scheduler.get_lr()[0])))
        train(train_loader, model, criterion, optimizer, epoch, args)
        acc1 = validate(val_loader, model, criterion, args)
        is_best = (acc1 > best_acc1)
        best_acc1 = max(acc1, best_acc1)
        if ((not args.multiprocessing_distributed) or (args.multiprocessing_distributed and ((args.rank % ngpus_per_node) == 0))):
            save_checkpoint({'epoch': (epoch + 1), 'arch': args.arch, 'state_dict': model.state_dict(), 'best_acc1': best_acc1, 'optimizer': optimizer.state_dict()}, is_best, epoch, out_dir=args.out_dir)
