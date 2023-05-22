import os
import glob
import torch
import torch.nn as nn
import time
import datetime
import logging
import json
import numpy as np
from torch.utils.data import DataLoader


def _save_checkpoint(self, epoch, acc):
    '\n        Saves a checkpoint of the network and other variables.\n        Only save the best and latest epoch.\n        '
    net_type = type(self.net).__name__
    if ((epoch - self.eval_freq) != self.best_epoch):
        pre_save = os.path.join(self.logdir, '{}_{:03d}.pkl'.format(net_type, (epoch - self.eval_freq)))
        if os.path.isfile(pre_save):
            os.remove(pre_save)
    cur_save = os.path.join(self.logdir, '{}_{:03d}.pkl'.format(net_type, epoch))
    state = {'epoch': epoch, 'acc': acc, 'net_type': net_type, 'net': self.net.state_dict(), 'optimizer': self.optimizer.state_dict(), 'use_gpu': self.use_gpu, 'save_time': datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}
    torch.save(state, cur_save)
    return True
