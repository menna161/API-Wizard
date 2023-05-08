from data import *
from utils.augmentations import SSDAugmentation
from layers.modules import MultiBoxLoss
from ssd import build_ssd
import os
import sys
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn
import torch.nn.init as init
import torch.utils.data as data
import argparse
from utils import helpers
import logging
import time
import datetime
from torchviz import make_dot
import visdom


def train(args):
    cfg = exp_cfg[args.cfg]
    dataset = GTDBDetection(args, args.training_data, split='train', transform=SSDAugmentation(cfg['min_dim'], mean=MEANS))
    if args.visdom:
        import visdom
        viz = visdom.Visdom()
    gpu_id = 0
    if args.cuda:
        gpu_id = helpers.get_freer_gpu()
        logging.debug(('Using GPU with id ' + str(gpu_id)))
        torch.cuda.set_device(gpu_id)
    ssd_net = build_ssd(args, 'train', cfg, gpu_id, cfg['min_dim'], cfg['num_classes'])
    logging.debug(ssd_net)
    ct = 0
    for child in ssd_net.vgg.children():
        if (ct >= args.layers_to_freeze):
            break
        child.requires_grad = False
        ct += 1
    if args.resume:
        logging.debug('Resuming training, loading {}...'.format(args.resume))
        ssd_net.load_state_dict(torch.load(args.resume))
    else:
        vgg_weights = torch.load(('base_weights/' + args.basenet))
        logging.debug('Loading base network...')
        ssd_net.vgg.load_state_dict(vgg_weights)
    step_index = 0
    if (not args.resume):
        logging.debug('Initializing weights...')
        ssd_net.extras.apply(weights_init)
        ssd_net.loc.apply(weights_init)
        ssd_net.conf.apply(weights_init)
        for val in cfg['lr_steps']:
            if (args.start_iter > val):
                step_index = (step_index + 1)
        torch.save(ssd_net.state_dict(), os.path.join(('weights_' + args.exp_name), ((('initial_' + str(args.model_type)) + args.dataset) + '.pth')))
    optimizer = optim.SGD(ssd_net.parameters(), lr=args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
    adjust_learning_rate(args, optimizer, args.gamma, step_index)
    criterion = MultiBoxLoss(args, cfg, args.pos_thresh, 0, 3)
    if args.cuda:
        ssd_net = torch.nn.DataParallel(ssd_net)
        cudnn.benchmark = True
    ssd_net.train()
    loc_loss = 0
    conf_loss = 0
    min_total_loss = float('inf')
    epoch = 0
    logging.debug('Loading the dataset...')
    epoch_size = (len(dataset) // args.batch_size)
    logging.debug(('Training SSD on:' + dataset.name))
    logging.debug('Using the specified args:')
    logging.debug(args)
    if args.visdom:
        vis_title = args.exp_name
        vis_legend = ['Location Loss', 'Confidence Loss', 'Total Loss']
        iter_plot = create_vis_plot('Iteration', 'Loss', viz, ('Training ' + vis_title), vis_legend)
        epoch_plot = create_vis_plot('Epoch', 'Loss', viz, ('Training ' + vis_title), vis_legend)
    data_loader = data.DataLoader(dataset, args.batch_size, num_workers=args.num_workers, shuffle=True, collate_fn=detection_collate, pin_memory=True)
    logging.debug(('Training set size is ' + str(len(dataset))))
    batch_iterator = iter(data_loader)
    for iteration in range(args.start_iter, cfg['max_iter']):
        ssd_net.train()
        t0 = time.time()
        if (iteration in cfg['lr_steps']):
            step_index += 1
            adjust_learning_rate(args, optimizer, args.gamma, step_index)
        try:
            (images, targets, _) = next(batch_iterator)
        except StopIteration:
            batch_iterator = iter(data_loader)
            (images, targets, _) = next(batch_iterator)
        if args.cuda:
            images = images.cuda()
            targets = [ann.cuda() for ann in targets]
        else:
            images = Variable(images)
            targets = [Variable(ann, volatile=True) for ann in targets]
        out = ssd_net(images)
        optimizer.zero_grad()
        (loss_l, loss_c) = criterion(out, targets)
        loss = ((args.alpha * loss_l) + loss_c)
        loss.backward()
        optimizer.step()
        loc_loss += loss_l.item()
        conf_loss += loss_c.item()
        t1 = time.time()
        if ((iteration % 10) == 0):
            logging.debug(('timer: %.4f sec.' % (t1 - t0)))
            logging.debug((('iter ' + repr(iteration)) + (' || Loss: %.4f ||' % loss.item())))
        if args.visdom:
            update_vis_plot(iteration, loss_l.item(), viz, loss_c.item(), iter_plot, epoch_plot, 'append')
        if ((iteration != 0) and ((iteration % 1000) == 0)):
            logging.debug(('Saving state, iter:' + str(iteration)))
            torch.save(ssd_net.state_dict(), os.path.join(('weights_' + args.exp_name), (((('ssd' + str(args.model_type)) + args.dataset) + repr(iteration)) + '.pth')))
        if ((iteration != 0) and ((iteration % epoch_size) == 0)):
            epoch += 1
            torch.save(ssd_net.state_dict(), os.path.join(('weights_' + args.exp_name), (((('epoch_ssd' + str(args.model_type)) + args.dataset) + repr(epoch)) + '.pth')))
            train_loss = (loc_loss + conf_loss)
            update_vis_plot(epoch, loc_loss, viz, conf_loss, epoch_plot, None, 'append', epoch_size)
            if (args.validation_data != ''):
                validation_loss = validate(args, ssd_net, criterion, cfg)
                if (epoch == 1):
                    validation_plot = create_validation_plot(epoch, validation_loss, 'Epoch', 'Loss', viz, ('Validating ' + vis_title), ['Validation'])
                else:
                    update_validation_plot(epoch, validation_loss, viz, validation_plot, 'append')
                if (validation_loss < min_total_loss):
                    min_total_loss = validation_loss
                    torch.save(ssd_net.state_dict(), os.path.join(('weights_' + args.exp_name), (((('best_ssd' + str(args.model_type)) + args.dataset) + repr(iteration)) + '.pth')))
            loc_loss = 0
            conf_loss = 0
    torch.save(ssd_net.state_dict(), (((args.exp_name + '') + args.dataset) + '.pth'))
    logging.debug((((('Final weights are saved at ' + args.exp_name) + '') + args.dataset) + '.pth'))
