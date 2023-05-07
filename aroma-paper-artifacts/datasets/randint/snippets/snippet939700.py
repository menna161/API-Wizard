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


def eval_epoch(self, epoch):
    device = torch.device(('cuda:0' if self.use_gpu else 'cpu'))
    self.net.to(device)
    self.criterion.to(device)
    self.net.eval()
    val_total_time = 0
    measures = {key: 0 for key in measure_list}
    with torch.no_grad():
        sys.stdout.flush()
        tbar = tqdm(self.valloader)
        rand = np.random.randint(len(self.valloader))
        for (step, data) in enumerate(tbar):
            (images, labels) = (data[0].to(device), data[1].to(device))
            before_op_time = time.time()
            y = self.net(images)
            depths = self.net.inference(y)
            duration = (time.time() - before_op_time)
            val_total_time += duration
            new = self.eval_func(labels, depths)
            for (k, v) in new.items():
                measures[k] += v.item()
            if ((step == rand) and (self.disp_func is not None)):
                visuals = {'inputs': images, 'sim_map': y['sim_map'], 'labels': labels, 'depths': depths}
                self.disp_func(self.writer, visuals, epoch)
            print_str = 'Test step [{}/{}].'.format((step + 1), len(self.valloader))
            tbar.set_description(print_str)
    fps = (self.n_val / val_total_time)
    measures = {key: round((value / self.n_val), 5) for (key, value) in measures.items()}
    return (measures, fps)
