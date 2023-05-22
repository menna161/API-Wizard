import os
import math
import time
import datetime
from functools import reduce
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.misc as misc
import torch
import torch.optim as optim
import torch.optim.lr_scheduler as lrs


def plot_psnr(self, epoch):
    axis = np.linspace(1, epoch, epoch)
    label = 'SR on {}'.format(self.args.data_test)
    fig = plt.figure()
    plt.title(label)
    for (idx_scale, scale) in enumerate(self.args.scale):
        plt.plot(axis, self.log[(:, idx_scale)].numpy(), label='Scale {}'.format(scale))
    plt.legend()
    plt.xlabel('Epochs')
    plt.ylabel('PSNR')
    plt.grid(True)
    plt.savefig('{}/test_{}.pdf'.format(self.dir, self.args.data_test))
    plt.close(fig)
