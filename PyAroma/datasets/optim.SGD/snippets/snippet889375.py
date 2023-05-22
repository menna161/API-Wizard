from __future__ import print_function
import argparse
import torch
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
import os
import math
import data_loader
import ResNet as models
from torch.utils import model_zoo


def train(model):
    src_iter = iter(src_loader)
    tgt_iter = iter(tgt_train_loader)
    correct = 0
    optimizer = torch.optim.SGD([{'params': model.sharedNet.parameters()}, {'params': model.cls_fc.parameters(), 'lr': lr[1]}], lr=lr[0], momentum=momentum, weight_decay=l2_decay)
    for i in range(1, (iteration + 1)):
        model.train()
        for (index, param_group) in enumerate(optimizer.param_groups):
            param_group['lr'] = (lr[index] / math.pow((1 + ((10 * (i - 1)) / iteration)), 0.75))
        try:
            (src_data, src_label) = src_iter.next()
        except Exception as err:
            src_iter = iter(src_loader)
            (src_data, src_label) = src_iter.next()
        try:
            (tgt_data, _) = tgt_iter.next()
        except Exception as err:
            tgt_iter = iter(tgt_train_loader)
            (tgt_data, _) = tgt_iter.next()
        if cuda:
            (src_data, src_label) = (src_data.cuda(), src_label.cuda())
            tgt_data = tgt_data.cuda()
        optimizer.zero_grad()
        (src_pred, mmd_loss) = model(src_data, tgt_data)
        cls_loss = F.nll_loss(F.log_softmax(src_pred, dim=1), src_label)
        lambd = ((2 / (1 + math.exp((((- 10) * i) / iteration)))) - 1)
        loss = (cls_loss + (lambd * mmd_loss))
        loss.backward()
        optimizer.step()
        if ((i % log_interval) == 0):
            print('Train iter: {} [({:.0f}%)]\tLoss: {:.6f}\tsoft_Loss: {:.6f}\tmmd_Loss: {:.6f}'.format(i, ((100.0 * i) / iteration), loss.item(), cls_loss.item(), mmd_loss.item()))
        if ((i % (log_interval * 20)) == 0):
            t_correct = test(model)
            if (t_correct > correct):
                correct = t_correct
            print('src: {} to tgt: {} max correct: {} max accuracy{: .2f}%\n'.format(src_name, tgt_name, correct, ((100.0 * correct) / tgt_dataset_len)))
