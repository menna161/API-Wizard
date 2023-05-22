from _warnings import warn
from typing import Tuple
import matplotlib
from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.network_architecture.neural_network import SegmentationNetwork
from sklearn.model_selection import KFold
from torch import nn
from torch.optim.lr_scheduler import _LRScheduler
from time import time, sleep
import torch
import numpy as np
from torch.optim import lr_scheduler
import matplotlib.pyplot as plt
import sys
from collections import OrderedDict
import torch.backends.cudnn as cudnn
from abc import abstractmethod
from datetime import datetime
from tqdm import trange
from apex import amp
import math
import matplotlib.pyplot as plt


def plot_progress(self):
    '\n        Should probably by improved\n        :return:\n        '
    try:
        font = {'weight': 'normal', 'size': 18}
        matplotlib.rc('font', **font)
        fig = plt.figure(figsize=(30, 24))
        ax = fig.add_subplot(111)
        ax2 = ax.twinx()
        x_values = list(range((self.epoch + 1)))
        ax.plot(x_values, self.all_tr_losses, color='b', ls='-', label='loss_tr')
        ax.plot(x_values, self.all_val_losses, color='r', ls='-', label='loss_val, train=False')
        if (len(self.all_val_losses_tr_mode) > 0):
            ax.plot(x_values, self.all_val_losses_tr_mode, color='g', ls='-', label='loss_val, train=True')
        if (len(self.all_val_eval_metrics) == len(x_values)):
            ax2.plot(x_values, self.all_val_eval_metrics, color='g', ls='--', label='evaluation metric')
        ax.set_xlabel('epoch')
        ax.set_ylabel('loss')
        ax2.set_ylabel('evaluation metric')
        ax.legend()
        ax2.legend(loc=9)
        fig.savefig(join(self.output_folder, 'progress.png'))
        plt.close()
    except IOError:
        self.print_to_log_file('failed to plot: ', sys.exc_info())
