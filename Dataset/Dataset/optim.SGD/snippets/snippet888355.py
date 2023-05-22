import argparse
import os
import random
import shutil
import time
import warnings
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
import torchvision.models as models
import torch.nn.functional as F
from tensorboardX import SummaryWriter
from torch.optim.lr_scheduler import MultiStepLR
from loss_function import loss_soft_regularization, loss_label_smoothing, loss_fn_kd


def main_worker(gpu, ngpus_per_node, args, writer, log_dir):
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
    print("=> creating model '{}'".format(args.arch))
    model = models.__dict__[args.arch]()
    print("=> creating teacher model '{}'".format(args.arch))
    teacher_model = models.__dict__[args.arch_teacher](pretrained=True)
    if args.distributed:
        if (args.gpu is not None):
            torch.cuda.set_device(args.gpu)
            model.cuda(args.gpu)
            teacher_model.cuda(args.gpu)
            args.batch_size = int((args.batch_size / ngpus_per_node))
            args.workers = int((((args.workers + ngpus_per_node) - 1) / ngpus_per_node))
            model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.gpu])
            teacher_model = torch.nn.parallel.DistributedDataParallel(teacher_model, device_ids=[args.gpu])
        else:
            model.cuda()
            teacher_model.cuda()
            model = torch.nn.parallel.DistributedDataParallel(model)
            teacher_model = torch.nn.parallel.DistributedDataParallel(teacher_model)
    elif (args.gpu is not None):
        torch.cuda.set_device(args.gpu)
        model = model.cuda(args.gpu)
        teacher_model = teacher_model.cuda(args.gpu)
    elif (args.arch.startswith('alexnet') or args.arch.startswith('vgg')):
        model.features = torch.nn.DataParallel(model.features)
        model.cuda()
        teacher_model.features = torch.nn.DataParallel(teacher_model.features)
        teacher_model.cuda()
    else:
        model = torch.nn.DataParallel(model).cuda()
        teacher_model = torch.nn.DataParallel(teacher_model).cuda()
    criterion = nn.CrossEntropyLoss().cuda(args.gpu)
    optimizer = torch.optim.SGD(model.parameters(), (args.lr * (args.batch_size / 256)), momentum=args.momentum, weight_decay=args.weight_decay)
    if args.resume:
        if os.path.isfile(args.resume):
            print("=> loading checkpoint '{}'".format(args.resume))
            checkpoint = torch.load(args.resume)
            args.start_epoch = checkpoint['epoch']
            best_acc1 = checkpoint['best_acc1']
            if (args.gpu is not None):
                best_acc1 = best_acc1.to(args.gpu)
            model.load_state_dict(checkpoint['state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer'])
            print("=> loaded checkpoint '{}' (epoch {})".format(args.resume, checkpoint['epoch']))
        else:
            print("=> no checkpoint found at '{}'".format(args.resume))
    cudnn.benchmark = True
    traindir = os.path.join(args.data, 'train')
    valdir = os.path.join(args.data, 'val')
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    train_dataset = datasets.ImageFolder(traindir, transforms.Compose([transforms.RandomResizedCrop(224), transforms.RandomHorizontalFlip(), transforms.ToTensor(), normalize]))
    if args.distributed:
        train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
    else:
        train_sampler = None
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=args.batch_size, shuffle=(train_sampler is None), num_workers=args.workers, pin_memory=True, sampler=train_sampler)
    val_loader = torch.utils.data.DataLoader(datasets.ImageFolder(valdir, transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), normalize])), batch_size=args.batch_size, shuffle=False, num_workers=args.workers, pin_memory=True)
    if args.evaluate:
        validate(val_loader, model, criterion, args)
        return
    scheduler = MultiStepLR(optimizer, milestones=[30, 60, 80], gamma=0.1)
    (acc1, acc5, test_loss) = validate(val_loader, teacher_model, criterion, args)
    print('>>>>>>>>>>>>>>>The teacher accuracy, top1:{}, top5:{}>>>>>>>>>>>>'.format(acc1, acc5))
    for epoch in range(args.start_epoch, args.epochs):
        if args.distributed:
            train_sampler.set_epoch(epoch)
        scheduler.step(epoch)
        (train_acc1, train_acc5, train_loss_CE) = train(train_loader, model, teacher_model, criterion, optimizer, epoch, args)
        (acc1, acc5, test_loss) = validate(val_loader, model, criterion, args)
        is_best = (acc1 > best_acc1)
        best_acc1 = max(acc1, best_acc1)
        if ((not args.multiprocessing_distributed) or (args.multiprocessing_distributed and ((args.rank % ngpus_per_node) == 0))):
            save_checkpoint({'epoch': (epoch + 1), 'arch': args.arch, 'state_dict': model.state_dict(), 'best_acc1': best_acc1, 'optimizer': optimizer.state_dict()}, is_best, dir=log_dir)
        writer.add_scalar('Train_acc_top1', train_acc1, epoch)
        writer.add_scalar('Train_acc_top5', train_acc5, epoch)
        writer.add_scalar('Train_loss_CE', train_loss_CE, epoch)
        writer.add_scalar('Test_acc_top1', acc1, epoch)
        writer.add_scalar('Test_acc_top5', acc5, epoch)
        writer.add_scalar('Test_loss_CE', test_loss, epoch)
    writer.close()
