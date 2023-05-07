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


def find_lr(self, num_iters=1000, init_value=1e-06, final_value=10.0, beta=0.98):
    '\n        stolen and adapted from here: https://sgugger.github.io/how-do-you-find-a-good-learning-rate.html\n        :param num_iters:\n        :param init_value:\n        :param final_value:\n        :param beta:\n        :return:\n        '
    import math
    self._maybe_init_amp()
    mult = ((final_value / init_value) ** (1 / num_iters))
    lr = init_value
    self.optimizer.param_groups[0]['lr'] = lr
    avg_loss = 0.0
    best_loss = 0.0
    losses = []
    log_lrs = []
    for batch_num in range(1, (num_iters + 1)):
        loss = (self.run_iteration(self.tr_gen, do_backprop=True, run_online_evaluation=False).data.item() + 1)
        avg_loss = ((beta * avg_loss) + ((1 - beta) * loss))
        smoothed_loss = (avg_loss / (1 - (beta ** batch_num)))
        if ((batch_num > 1) and (smoothed_loss > (4 * best_loss))):
            break
        if ((smoothed_loss < best_loss) or (batch_num == 1)):
            best_loss = smoothed_loss
        losses.append(smoothed_loss)
        log_lrs.append(math.log10(lr))
        lr *= mult
        self.optimizer.param_groups[0]['lr'] = lr
    import matplotlib.pyplot as plt
    lrs = [(10 ** i) for i in log_lrs]
    fig = plt.figure()
    plt.xscale('log')
    plt.plot(lrs[10:(- 5)], losses[10:(- 5)])
    plt.savefig(join(self.output_folder, 'lr_finder.png'))
    plt.close()
    return (log_lrs, losses)
