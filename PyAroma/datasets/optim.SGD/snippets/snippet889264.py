from __future__ import print_function
import torch
import torch.nn.functional as F
from torch.autograd import Variable
import os
import math
import data_loader
import resnet as models


def train(model):
    source1_iter = iter(source1_loader)
    source2_iter = iter(source2_loader)
    target_iter = iter(target_train_loader)
    correct = 0
    optimizer = torch.optim.SGD([{'params': model.sharedNet.parameters()}, {'params': model.cls_fc_son1.parameters(), 'lr': lr[1]}, {'params': model.cls_fc_son2.parameters(), 'lr': lr[1]}, {'params': model.sonnet1.parameters(), 'lr': lr[1]}, {'params': model.sonnet2.parameters(), 'lr': lr[1]}], lr=lr[0], momentum=momentum, weight_decay=l2_decay)
    for i in range(1, (iteration + 1)):
        model.train()
        optimizer.param_groups[0]['lr'] = (lr[0] / math.pow((1 + ((10 * (i - 1)) / iteration)), 0.75))
        optimizer.param_groups[1]['lr'] = (lr[1] / math.pow((1 + ((10 * (i - 1)) / iteration)), 0.75))
        optimizer.param_groups[2]['lr'] = (lr[1] / math.pow((1 + ((10 * (i - 1)) / iteration)), 0.75))
        optimizer.param_groups[3]['lr'] = (lr[1] / math.pow((1 + ((10 * (i - 1)) / iteration)), 0.75))
        optimizer.param_groups[4]['lr'] = (lr[1] / math.pow((1 + ((10 * (i - 1)) / iteration)), 0.75))
        try:
            (source_data, source_label) = source1_iter.next()
        except Exception as err:
            source1_iter = iter(source1_loader)
            (source_data, source_label) = source1_iter.next()
        try:
            (target_data, __) = target_iter.next()
        except Exception as err:
            target_iter = iter(target_train_loader)
            (target_data, __) = target_iter.next()
        if cuda:
            (source_data, source_label) = (source_data.cuda(), source_label.cuda())
            target_data = target_data.cuda()
        (source_data, source_label) = (Variable(source_data), Variable(source_label))
        target_data = Variable(target_data)
        optimizer.zero_grad()
        (cls_loss, mmd_loss, l1_loss) = model(source_data, target_data, source_label, mark=1)
        gamma = ((2 / (1 + math.exp((((- 10) * i) / iteration)))) - 1)
        loss = (cls_loss + (gamma * (mmd_loss + l1_loss)))
        loss.backward()
        optimizer.step()
        if ((i % log_interval) == 0):
            print('Train source1 iter: {} [({:.0f}%)]\tLoss: {:.6f}\tsoft_Loss: {:.6f}\tmmd_Loss: {:.6f}\tl1_Loss: {:.6f}'.format(i, ((100.0 * i) / iteration), loss.item(), cls_loss.item(), mmd_loss.item(), l1_loss.item()))
        try:
            (source_data, source_label) = source2_iter.next()
        except Exception as err:
            source2_iter = iter(source2_loader)
            (source_data, source_label) = source2_iter.next()
        try:
            (target_data, __) = target_iter.next()
        except Exception as err:
            target_iter = iter(target_train_loader)
            (target_data, __) = target_iter.next()
        if cuda:
            (source_data, source_label) = (source_data.cuda(), source_label.cuda())
            target_data = target_data.cuda()
        (source_data, source_label) = (Variable(source_data), Variable(source_label))
        target_data = Variable(target_data)
        optimizer.zero_grad()
        (cls_loss, mmd_loss, l1_loss) = model(source_data, target_data, source_label, mark=2)
        gamma = ((2 / (1 + math.exp((((- 10) * i) / iteration)))) - 1)
        loss = (cls_loss + (gamma * (mmd_loss + l1_loss)))
        loss.backward()
        optimizer.step()
        if ((i % log_interval) == 0):
            print('Train source2 iter: {} [({:.0f}%)]\tLoss: {:.6f}\tsoft_Loss: {:.6f}\tmmd_Loss: {:.6f}\tl1_Loss: {:.6f}'.format(i, ((100.0 * i) / iteration), loss.item(), cls_loss.item(), mmd_loss.item(), l1_loss.item()))
        if ((i % (log_interval * 20)) == 0):
            t_correct = test(model)
            if (t_correct > correct):
                correct = t_correct
            print(source1_name, source2_name, 'to', target_name, ('%s max correct:' % target_name), correct.item(), '\n')
