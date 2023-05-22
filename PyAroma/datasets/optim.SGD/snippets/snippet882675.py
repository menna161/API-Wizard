from __future__ import division
import os, sys
from modules.cutmix import CutMix
from modules.cutout import Cutout
from modules.patchup import PatchUpMode
from utility.adversarial_attack import run_test_adversarial
from torchvision import transforms
import torch.backends.cudnn as cudnn
import matplotlib as mpl
from utility.utils import *
import models
from collections import OrderedDict
from data_loader import *
from utility.utils import copy_script_to_folder
import shutil
from utility.plots import *
import numpy as np
import argparse
import cPickle as pickle
import _pickle as pickle


def main():
    exp_name = experiment_name_non_mnist(dataset=args.dataset, arch=args.arch, epochs=args.epochs, dropout=args.dropout, batch_size=args.batch_size, lr=args.learning_rate, momentum=args.momentum, decay=args.decay, data_aug=args.data_aug, train=args.train, alpha=args.alpha, job_id=args.job_id, add_name=args.add_name, patchup_mode=args.patchup_type, keep_prob=args.keep_prob, gamma=args.gamma, k=args.k, dropblock_all=args.drop_block_all)
    exp_dir = os.path.join(args.root_dir, exp_name)
    if (not os.path.exists(exp_dir)):
        os.makedirs(exp_dir)
    copy_script_to_folder(os.path.abspath(__file__), exp_dir)
    result_png_path = os.path.join(exp_dir, 'results.png')
    global best_acc
    global best_model
    log = open(os.path.join(exp_dir, 'log.txt'.format(args.manualSeed)), 'w')
    print_log('save path : {}'.format(exp_dir), log)
    state = {k: v for (k, v) in args._get_kwargs()}
    print_log(state, log)
    print_log('Random Seed: {}'.format(args.manualSeed), log)
    print_log('python version : {}'.format(sys.version.replace('\n', ' ')), log)
    print_log('torch  version : {}'.format(torch.__version__), log)
    print_log('cudnn  version : {}'.format(torch.backends.cudnn.version()), log)
    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    num_workers = 0
    if (device == torch.device('cuda')):
        num_workers = 2
    per_img_std = False
    (train_loader, valid_loader, _, test_loader, num_classes) = load_data_subset(args.data_aug, args.batch_size, num_workers, args.dataset, args.data_dir, labels_per_class=args.labels_per_class, valid_labels_per_class=args.valid_labels_per_class)
    if (args.dataset == 'tiny-imagenet-200'):
        stride = 2
    else:
        stride = 1
    drop_block = args.drop_block
    keep_prob = args.keep_prob
    gamma = args.gamma
    patchup_block = args.patchup_block
    patchup_prob = args.patchup_prob
    print_log("=> creating model '{}'".format(args.arch), log)
    net = models.__dict__[args.arch](num_classes, args.dropout, per_img_std, stride, drop_block, keep_prob, gamma, patchup_block).to(device)
    print_log('=> network :\n {}'.format(net), log)
    args.num_classes = num_classes
    optimizer = torch.optim.SGD(net.parameters(), state['learning_rate'], momentum=state['momentum'], weight_decay=state['decay'], nesterov=True)
    recorder = RecorderMeter(args.epochs)
    if args.resume:
        if os.path.isfile(args.resume):
            print_log("=> loading checkpoint '{}'".format(args.resume), log)
            checkpoint = torch.load(args.resume)
            recorder = checkpoint['recorder']
            args.start_epoch = checkpoint['epoch']
            net.load_state_dict(checkpoint['state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer'])
            best_acc = recorder.max_accuracy(False)
            print_log("=> loaded checkpoint '{}' accuracy={} (epoch {})".format(args.resume, best_acc, checkpoint['epoch']), log)
        else:
            print_log("=> no checkpoint found at '{}'".format(args.resume), log)
    else:
        print_log('=> do not use any checkpoint for {} model'.format(args.arch), log)
    if args.evaluate:
        validate(test_loader, net, criterion, log)
        return
    start_time = time.time()
    epoch_time = AverageMeter()
    train_loss = []
    train_acc = []
    test_loss = []
    test_acc = []
    for epoch in range(args.start_epoch, args.epochs):
        current_learning_rate = adjust_learning_rate(optimizer, epoch, args.step_factors, args.schedule)
        (need_hour, need_mins, need_secs) = convert_secs2time((epoch_time.avg * (args.epochs - epoch)))
        need_time = '[Need: {:02d}:{:02d}:{:02d}]'.format(need_hour, need_mins, need_secs)
        print_log(('\n==>>{:s} [Epoch={:03d}/{:03d}] {:s} [learning_rate={:6.4f}]'.format(time_string(), epoch, args.epochs, need_time, current_learning_rate) + ' [Best Accuracy={:.2f}, Error={:.2f}]'.format(recorder.max_accuracy(False), (100 - recorder.max_accuracy(False)))), log)
        (tr_acc, tr_acc5, tr_los) = train(train_loader, net, optimizer, epoch, args, log)
        (val_acc, top5_avg, error1, val_los) = validate(valid_loader, net, log)
        train_loss.append(tr_los)
        train_acc.append(tr_acc)
        test_loss.append(val_los)
        test_acc.append(val_acc)
        dummy = recorder.update(epoch, tr_los, tr_acc, val_los, val_acc)
        is_best = False
        if (val_acc > best_acc):
            is_best = True
            (best_acc, best_top5_avg, best_error1, best_val_los) = (val_acc, top5_avg, error1, val_los)
            best_model = models.__dict__[args.arch](num_classes, args.dropout, per_img_std, stride).to(device)
            best_model.load_state_dict(net.state_dict())
            best_model.eval()
        if args.checkpoint:
            save_checkpoint({'epoch': (epoch + 1), 'arch': args.arch, 'state_dict': net.state_dict(), 'recorder': recorder, 'optimizer': optimizer.state_dict()}, is_best, exp_dir, 'checkpoint.pth.tar')
        epoch_time.update((time.time() - start_time))
        start_time = time.time()
        recorder.plot_curve(result_png_path)
        train_log = OrderedDict()
        train_log['train_loss'] = train_loss
        train_log['train_acc'] = train_acc
        train_log['test_loss'] = test_loss
        train_log['test_acc'] = test_acc
        pickle.dump(train_log, open(os.path.join(exp_dir, 'log.pkl'), 'wb'))
        plotting(exp_dir)
    print_log('best model stat on validation set:', log)
    validate(valid_loader, best_model, log)
    print_log('best model stat on test set:', log)
    validate(test_loader, best_model, log)
    if args.affine_test:
        affine_data_loaders = load_transformed_test_sets(args.affine_path, batch_size=100, workers=2)
        for t_loader in affine_data_loaders:
            print_log(f'model performance on {t_loader.transformer} test set:', log)
            validate(t_loader, best_model, log)
    if args.fsgm_attack:
        epsilons = [0, 0.05, 0.1, 0.12, 0.15, 0.18, 0.2]
        accuracies = []
        for eps in epsilons:
            result = run_test_adversarial(best_model, test_loader, eps)
            accuracies.append(result)
            print_log(result, log)
        print_log('the FSGM result :', log)
        print_log(accuracies, log)
    log.close()
