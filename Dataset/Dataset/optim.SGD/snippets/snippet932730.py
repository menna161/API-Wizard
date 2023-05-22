import torch
from torch import nn
from reid import models
from reid.trainers import Trainer
from reid.evaluators import extract_features, Evaluator
from reid.dist_metric import DistanceMetric
import numpy as np
from collections import OrderedDict
import os.path as osp
import pickle
import copy, sys
from reid.utils.serialization import load_checkpoint
from reid.utils.data import transforms as T
from torch.utils.data import DataLoader
from reid.utils.data.preprocessor import Preprocessor
import random
import pickle as pkl
from reid.exclusive_loss import ExLoss


def train(self, train_data, step, loss, dropout=0.5):
    epochs = (self.initial_steps if (step == 0) else self.later_steps)
    init_lr = (0.1 if (step == 0) else 0.01)
    step_size = (self.step_size if (step == 0) else sys.maxsize)
    ' create model and dataloader '
    dataloader = self.get_dataloader(train_data, training=True)
    base_param_ids = set(map(id, self.model.module.CNN.base.parameters()))
    base_params_need_for_grad = filter((lambda p: p.requires_grad), self.model.module.CNN.base.parameters())
    new_params = [p for p in self.model.parameters() if (id(p) not in base_param_ids)]
    param_groups = [{'params': base_params_need_for_grad, 'lr_mult': 0.1}, {'params': new_params, 'lr_mult': 1.0}]
    optimizer = torch.optim.SGD(param_groups, lr=init_lr, momentum=0.9, weight_decay=0.0005, nesterov=True)

    def adjust_lr(epoch, step_size):
        lr = (init_lr / (10 ** (epoch // step_size)))
        for g in optimizer.param_groups:
            g['lr'] = (lr * g.get('lr_mult', 1))
    ' main training process '
    trainer = Trainer(self.model, self.criterion, fixed_layer=self.fixed_layer)
    for epoch in range(epochs):
        adjust_lr(epoch, step_size)
        trainer.train(epoch, dataloader, optimizer, print_freq=max(5, ((len(dataloader) // 30) * 10)))
