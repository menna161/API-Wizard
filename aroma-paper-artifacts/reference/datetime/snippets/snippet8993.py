import sys
import json
import time
import datetime
import os
import random
import pickle
import numpy as np
import torch
from torch.autograd import Variable
import torch.optim as optim
from torch import nn
from sklearn.cluster import AffinityPropagation
from layers.modules import MultiBoxLoss
from layers import box_utils
from . import helpers
from data import VOCAnnotationTransform, VOCDetection, BaseTransform, VOC_CLASSES, detection_collate
from utils import augmentations
from . import uncertainty_helpers
import hdbscan


def train_model(args, train_dataset, val_dataset, ensemble_idx):
    train_loc_loss_list = []
    train_conf_loss_list = []
    val_loc_loss_list = []
    val_conf_loss_list = []
    if (args.modeltype == 'SSD300KL'):
        args.summary['train_model']['predicted_alphas'] = []
    label_dict = helpers.read_labeled(args.path_to_labeled_idx_file, args.annotate_all_objects, args.dataset, args)
    labeled_idx = label_dict['train_set']
    if (not args.train_on_full_dataset):
        train_set = helpers.data_subset(train_dataset, labeled_idx)
    else:
        train_set = train_dataset
    criterion = MultiBoxLoss(num_classes=args.cfg['num_classes'], overlap_thresh=0.5, prior_for_matching=True, bkg_label=0, neg_mining=True, neg_pos=3, neg_overlap=0.5, encode_target=False, use_gpu=(args.device == 'cuda'), modeltype=args.modeltype)
    net = helpers.build_train_net(args, ensemble_idx)
    if (args.optimizer == 'SGD'):
        optimizer = optim.SGD(net.parameters(), lr=args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
    elif (args.optimizer == 'ADAM'):
        optimizer = optim.Adam(net.parameters(), lr=args.lr, amsgrad=True, weight_decay=args.weight_decay)
    else:
        raise NotImplementedError()
    train_data_loader = helpers.InfiniteDataLoader(train_set, batch_size=args.batch_size, num_workers=args.num_workers, shuffle=True, collate_fn=detection_collate, pin_memory=True, drop_last=False)
    val_data_loader = torch.utils.data.DataLoader(val_dataset, args.batch_size, num_workers=args.num_workers, shuffle=True, collate_fn=detection_collate, pin_memory=True, drop_last=False)
    if (len(labeled_idx) > 1):
        validation_loss_frequency = (len(labeled_idx) - 1)
    else:
        validation_loss_frequency = 100
    train_batch_iterator = iter(train_data_loader)
    print('Active learning iteration: ', str(args.al_iteration), '\t\t training for: ', str(args.train_epochs), ' epochs\t\t with batch size: ', str(args.batch_size), '\t\t on:', len(train_set.ids), ' images')
    print('\n\n')
    lr_step = 0
    total_iterations = 0
    no_improvement_counter = 0
    decrease_lr = False
    stop_training = False
    if (args.fixed_number_of_epochs == None):
        for epoch in range(args.train_epochs):
            print('New epoch, Local time: ', datetime.datetime.now())
            if decrease_lr:
                lr_step += 1
                helpers.adjust_learning_rate(args, optimizer, lr_step)
                decrease_lr = False
            for iteration in range(round((len(labeled_idx) / args.batch_size))):
                if (((iteration == 0) and (epoch != 0)) or args.debug):
                    if (args.early_stopping_condition == 'just_lowest_val'):
                        print('Doing validation pass...')
                        (val_loss, val_loc_loss, val_conf_loss, save) = helpers.just_keep_lowest_val_loss_weights(args, net, criterion, val_data_loader, ensemble_idx)
                        print('Finished validation pass')
                        val_conf_loss_list.append(val_conf_loss)
                        val_loc_loss_list.append(val_loc_loss)
                        if (args.debug == True):
                            save = True
                        if save:
                            path = str(((((((((((((((((args.experiment_dir + 'weights/') + str(args.modeltype)) + '_al-iter_') + str(args.al_iteration)) + '_train-loss_') + str(loss.item())) + '_') + '_val-loss_') + str(val_loss)) + '_') + str(args.dataset)) + '_train-iter_') + str(total_iterations)) + '_ensemble-id_') + str(ensemble_idx)) + '_.pth'))
                            path_to_weights = helpers.save_weights(net, args, path, mode='neural_net')
                            try:
                                args.paths_to_weights[ensemble_idx] = path_to_weights
                            except:
                                args.paths_to_weights.append(path_to_weights)
                        else:
                            no_improvement_counter += 1
                            print('No improvement past ', no_improvement_counter, ' validation passes...')
                        if ((no_improvement_counter > args.epochs_no_improvement) and (lr_step < 2)):
                            decrease_lr = True
                            no_improvement_counter = 0
                        if ((no_improvement_counter > args.epochs_no_improvement) and (lr_step > 1)):
                            stop_training = True
                    else:
                        raise NotImplementedError()
                if stop_training:
                    print('No improvement\n\n Early stopping')
                    break
                total_iterations += 1
                if (args.debug and (iteration > 11)):
                    break
                (images, targets) = next(train_batch_iterator)
                if (args.device == 'cuda'):
                    with torch.cuda.device(0):
                        images = images.cuda()
                        with torch.no_grad():
                            targets = [ann.cuda() for ann in targets]
                    images = Variable(images)
                    with torch.no_grad():
                        targets = [Variable(target) for target in targets]
                else:
                    images = Variable(images)
                    with torch.no_grad():
                        targets = [Variable(ann) for ann in targets]
                t0 = time.time()
                out = net(images)
                optimizer.zero_grad()
                (loss_l, loss_c) = criterion(out, targets, args)
                loss = (loss_l + loss_c)
                loss.backward()
                optimizer.step()
                t1 = time.time()
                loc_loss = loss_l.item()
                conf_loss = loss_c.item()
                if ((iteration % 10) == 0):
                    print(('timer: %.4f sec.' % (t1 - t0)))
                    print((((('Epoch ' + str(epoch)) + '  iter ') + repr(iteration)) + (' || Loss: %.4f ||' % loss.item())))
                    train_loc_loss_list.append(loc_loss)
                    train_conf_loss_list.append(conf_loss)
            if stop_training:
                break
        best_nn_weights = helpers.delete_non_optimal_weights(args, mode='neural_net', ensemble_id=ensemble_idx)
        args.paths_to_weights[ensemble_idx] = ((args.experiment_dir + 'weights/') + best_nn_weights)
    elif args.fixed_number_of_epochs:
        adj_lr = [round((args.fixed_number_of_epochs * (2 / 3))), round((args.fixed_number_of_epochs * (5 / 6)))]
        for epoch in range(args.fixed_number_of_epochs):
            print('New epoch, Local time: ', datetime.datetime.now())
            if (epoch in adj_lr):
                lr_step += 1
                helpers.adjust_learning_rate(args, optimizer, lr_step)
            for iteration in range(max(1, round((len(train_set.ids) / args.batch_size)))):
                total_iterations += 1
                if (args.debug and (iteration > 11)):
                    break
                (images, targets) = next(train_batch_iterator)
                if (args.device == 'cuda'):
                    with torch.cuda.device(0):
                        images = images.to('cuda:0')
                        with torch.no_grad():
                            targets = [ann.to('cuda:0') for ann in targets]
                    images = Variable(images)
                    with torch.no_grad():
                        targets = [Variable(target) for target in targets]
                else:
                    images = Variable(images)
                    with torch.no_grad():
                        targets = [Variable(ann) for ann in targets]
                t0 = time.time()
                out = net(images)
                optimizer.zero_grad()
                (loss_l, loss_c) = criterion(out, targets)
                if ((args.modeltype == 'SSD300KL') and ((epoch == 0) and (iteration == 0))):
                    print('loss_l: ', loss_l)
                    print('loss_c: ', loss_c)
                loss = (loss_l + loss_c)
                loss.backward()
                optimizer.step()
                t1 = time.time()
                loc_loss = loss_l.item()
                conf_loss = loss_c.item()
                if args.debug:
                    train_loc_loss_list.append(loc_loss)
                    train_conf_loss_list.append(conf_loss)
                if ((iteration % 10) == 0):
                    print(('timer: %.4f sec.' % (t1 - t0)))
                    print((((((('Epoch ' + str(epoch)) + '  iter ') + repr(iteration)) + (' || Loss: %.4f ||' % loss.item())) + (' || conf loss: %.4f ||' % conf_loss)) + (' || loc loss: %.4f ||' % loc_loss)))
                    if args.train_basenets:
                        print('loc_loss: ', loc_loss, '      val loss: ', val_loss)
                    train_loc_loss_list.append(loc_loss)
                    train_conf_loss_list.append(conf_loss)
                val_loss = 999
                path = str(((((((((((((((((args.experiment_dir + 'weights/') + str(args.modeltype)) + '_al-iter_') + str(args.al_iteration)) + '_train-loss_') + str(loss.item())) + '_') + '_val-loss_') + str(val_loss)) + '_') + str(args.dataset)) + '_train-iter_') + str(total_iterations)) + '_ensemble-id_') + str(ensemble_idx)) + '_.pth'))
                if (((iteration == 0) and (epoch > (args.fixed_number_of_epochs / 2))) or (args.debug and (iteration == 0))):
                    if (args.early_stopping_condition == 'just_lowest_val'):
                        print('Doing validation pass...')
                        (val_loss, val_loc_loss, val_conf_loss, save) = helpers.just_keep_lowest_val_loss_weights(args, net, criterion, val_data_loader, ensemble_idx)
                        print('Finished validation pass')
                        val_loss = (val_conf_loss + val_loc_loss)
                        print('val los:  ', val_loss)
                        val_conf_loss_list.append(val_conf_loss)
                        val_loc_loss_list.append(val_loc_loss)
                        path = str(((((((((((((((((args.experiment_dir + 'weights/') + str(args.modeltype)) + '_al-iter_') + str(args.al_iteration)) + '_train-loss_') + str(loss.item())) + '_') + '_val-loss_') + str(val_loss)) + '_') + str(args.dataset)) + '_train-iter_') + str(total_iterations)) + '_ensemble-id_') + str(ensemble_idx)) + '_.pth'))
                        if save:
                            path_to_weights = helpers.save_weights(net, args, path, mode='neural_net')
            if args.save_every_epoch:
                path_to_weights = helpers.save_weights(net, args, path, mode='neural_net')
        best_nn_weights = helpers.delete_non_optimal_weights(args, mode='neural_net', ensemble_id=ensemble_idx)
        path_to_weights = ((args.experiment_dir + 'weights/') + best_nn_weights)
        try:
            args.paths_to_weights[ensemble_idx] = path_to_weights
        except:
            args.paths_to_weights.append(path_to_weights)
    elif args.fixed_number_of_train_iterations:
        for iteration in range(args.fixed_number_of_train_iterations):
            total_iterations += 1
            if (iteration == 26666):
                print('Adjust learning rate: ')
                helpers.adjust_learning_rate(args, optimizer, lr_step)
            (images, targets) = next(train_batch_iterator)
            if (args.device == 'cuda'):
                with torch.cuda.device(0):
                    images = images.cuda()
                    with torch.no_grad():
                        targets = [ann.cuda() for ann in targets]
                images = Variable(images)
                with torch.no_grad():
                    targets = [Variable(target) for target in targets]
            else:
                images = Variable(images)
                with torch.no_grad():
                    targets = [Variable(ann) for ann in targets]
            t0 = time.time()
            out = net(images)
            optimizer.zero_grad()
            (loss_l, loss_c) = criterion(out, targets)
            loss = (loss_l + loss_c)
            loss.backward()
            optimizer.step()
            t1 = time.time()
            loc_loss = loss_l.item()
            conf_loss = loss_c.item()
            if ((iteration % 10) == 0):
                print(('timer: %.4f sec.' % (t1 - t0)))
                print((((('Iteration: ' + repr(iteration)) + (' || Loss: %.4f ||' % loss.item())) + (' || conf loss: %.4f ||' % conf_loss)) + (' || loc loss: %.4f ||' % loc_loss)))
                train_loc_loss_list.append(loc_loss)
                train_conf_loss_list.append(conf_loss)
            if ((((iteration % validation_loss_frequency) == 0) and (iteration > 3000)) or args.debug):
                if (args.early_stopping_condition == 'just_lowest_val'):
                    print('Doing validation pass...')
                    (val_loss, val_loc_loss, val_conf_loss, save) = helpers.just_keep_lowest_val_loss_weights(args, net, criterion, val_data_loader, ensemble_idx)
                    print('Finished validation pass')
                    val_conf_loss_list.append(val_conf_loss)
                    val_loc_loss_list.append(val_loc_loss)
                    if (args.debug == True):
                        save = True
                    if save:
                        path = str(((((((((((((((((args.experiment_dir + 'weights/') + str(args.modeltype)) + '_al-iter_') + str(args.al_iteration)) + '_train-loss_') + str(loss.item())) + '_') + '_val-loss_') + str(val_loss)) + '_') + str(args.dataset)) + '_train-iter_') + str(total_iterations)) + '_ensemble-id_') + str(ensemble_idx)) + '_.pth'))
                        path_to_weights = helpers.save_weights(net, args, path, mode='neural_net')
                        try:
                            args.paths_to_weights[ensemble_idx] = path_to_weights
                        except:
                            args.paths_to_weights.append(path_to_weights)
    args.summary['train_model']['losses'][ensemble_idx] = {}
    args.summary['train_model']['losses'][ensemble_idx]['val_loc_loss'] = val_loc_loss_list
    args.summary['train_model']['losses'][ensemble_idx]['val_conf_loss'] = val_conf_loss_list
    args.summary['train_model']['losses'][ensemble_idx]['train_loc_loss'] = train_loc_loss_list
    args.summary['train_model']['losses'][ensemble_idx]['train_conf_loss'] = train_conf_loss_list
    args.summary['train_model']['total_iterations'] = total_iterations
