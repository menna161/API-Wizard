from __future__ import print_function, absolute_import
import time
from time import gmtime, strftime
from datetime import datetime
import gc
import os.path as osp
import sys
from PIL import Image
import numpy as np
import torch
from torchvision import transforms
from . import evaluation_metrics
from .evaluation_metrics import Accuracy, EditDistance
from .utils import to_numpy
from .utils.meters import AverageMeter
from .utils.serialization import load_checkpoint, save_checkpoint
from config import get_args


def train(self, epoch, data_loader, optimizer, current_lr=0.0, print_freq=100, train_tfLogger=None, is_debug=False, evaluator=None, test_loader=None, eval_tfLogger=None, test_dataset=None, test_freq=1000):
    self.model.train()
    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    end = time.time()
    for (i, inputs) in enumerate(data_loader):
        self.model.train()
        self.iters += 1
        data_time.update((time.time() - end))
        input_dict = self._parse_data(inputs)
        output_dict = self._forward(input_dict)
        batch_size = input_dict['images'].size(0)
        total_loss = 0
        loss_dict = {}
        for (k, loss) in output_dict['losses'].items():
            loss = loss.mean(dim=0, keepdim=True)
            total_loss += (self.loss_weights[k] * loss)
            loss_dict[k] = loss.item()
        losses.update(total_loss.item(), batch_size)
        optimizer.zero_grad()
        total_loss.backward()
        if (self.grad_clip > 0):
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_clip)
        optimizer.step()
        batch_time.update((time.time() - end))
        end = time.time()
        if ((self.iters % print_freq) == 0):
            print('[{}]\tEpoch: [{}][{}/{}]\tTime {:.3f} ({:.3f})\tData {:.3f} ({:.3f})\tLoss {:.3f} ({:.3f})\t'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), epoch, (i + 1), len(data_loader), batch_time.val, batch_time.avg, data_time.val, data_time.avg, losses.val, losses.avg))
        if (((self.iters % print_freq) * 10) == 0):
            if (train_tfLogger is not None):
                step = ((epoch * len(data_loader)) + (i + 1))
                info = {'lr': current_lr, 'loss': total_loss.item()}
                for (k, loss) in loss_dict.items():
                    info[k] = loss
                for (tag, value) in info.items():
                    train_tfLogger.scalar_summary(tag, value, step)
        if ((self.iters % test_freq) == 0):
            if ('loss_rec' not in output_dict['losses']):
                is_best = True
                self.best_res = evaluator.evaluate(test_loader, step=self.iters, tfLogger=eval_tfLogger, dataset=test_dataset)
            else:
                res = evaluator.evaluate(test_loader, step=self.iters, tfLogger=eval_tfLogger, dataset=test_dataset)
                if (self.metric == 'accuracy'):
                    is_best = (res > self.best_res)
                    self.best_res = max(res, self.best_res)
                elif (self.metric == 'editdistance'):
                    is_best = (res < self.best_res)
                    self.best_res = min(res, self.best_res)
                else:
                    raise ValueError('Unsupported evaluation metric:', self.metric)
                print('\n * Finished iters {:3d}  accuracy: {:5.1%}  best: {:5.1%}{}\n'.format(self.iters, res, self.best_res, (' *' if is_best else '')))
            save_checkpoint({'state_dict': self.model.module.state_dict(), 'iters': self.iters, 'best_res': self.best_res}, is_best, fpath=osp.join(self.logs_dir, 'checkpoint.pth.tar'))
