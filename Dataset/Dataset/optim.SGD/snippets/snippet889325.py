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

if (__name__ == '__main__'):
    model = models.DDCNet(num_classes=31)
    correct = 0
    print(model)
    if cuda:
        model.cuda()
    model = load_pretrain(model)
    optimizer = torch.optim.SGD([{'params': model.sharedNet.parameters()}, {'params': model.cls_fc.parameters(), 'lr': lr[1]}], lr=lr[0], momentum=momentum, weight_decay=l2_decay)
    for epoch in range(1, (epochs + 1)):
        for (index, param_group) in enumerate(optimizer.param_groups):
            param_group['lr'] = (lr[index] / math.pow((1 + ((10 * (epoch - 1)) / epochs)), 0.75))
        train(epoch, model, optimizer)
        t_correct = test(model)
        if (t_correct > correct):
            correct = t_correct
        print('source: {} to target: {} max correct: {} max accuracy{: .2f}%\n'.format(source_name, target_name, correct, ((100.0 * correct) / len_target_dataset)))
