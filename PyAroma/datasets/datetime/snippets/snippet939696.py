import os
import sys
import time
import datetime
import numpy as np
import scipy.io
import shutil
from tensorboardX import SummaryWriter
from trainers import Trainer, DataPrefetcher
from utils import predict_multi_scale, predict_whole_img, compute_errors, display_figure, colored_depthmap, merge_images, measure_list
import torch
from torch.nn import DataParallel
import matplotlib.pyplot as plt
from tqdm import tqdm
from copy import deepcopy
import json
from torchstat import stat
import tensorwatch as tw


def __init__(self, params, net, datasets, criterion, optimizer, scheduler, sets=['train', 'val', 'test'], verbose=100, stat=False, eval_func=compute_errors, disp_func=display_figure):
    self.time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    self.params = params
    self.verbose = verbose
    self.eval_func = eval_func
    self.disp_func = disp_func
    if (params.workdir is not None):
        workdir = os.path.expanduser(params.workdir)
    if (params.logdir is None):
        logdir = os.path.join(workdir, 'log_{}_{}'.format((params.encoder + params.decoder), params.dataset))
    else:
        logdir = os.path.join(workdir, params.logdir)
    resdir = None
    if (self.params.mode == 'test'):
        if (params.resdir is None):
            resdir = os.path.join(logdir, 'res')
        else:
            resdir = os.path.join(logdir, params.resdir)
    super().__init__(net, datasets, optimizer, scheduler, criterion, batch_size=params.batch, batch_size_val=params.batch_val, max_epochs=params.epochs, threads=params.threads, eval_freq=params.eval_freq, use_gpu=params.gpu, resume=params.resume, mode=params.mode, sets=sets, workdir=workdir, logdir=logdir, resdir=resdir)
    self.params.logdir = self.logdir
    self.params.resdir = self.resdir
    if (self.params.mode == 'train'):
        with open(os.path.join(self.logdir, 'params_{}.json'.format(self.time)), 'w') as f:
            json.dump(vars(self.params), f)
    if stat:
        from torchstat import stat
        import tensorwatch as tw
        stat(self.net, (3, *self.datasets[sets[0]].input_size))
        exit()
        tw.draw_model(self.net, (1, 3, *self.datasets[sets[0]].input_size))
    self.print('###### Experiment Parameters ######')
    for (k, v) in vars(self.params).items():
        self.print('{0:<22s} : {1:}'.format(k, v))
