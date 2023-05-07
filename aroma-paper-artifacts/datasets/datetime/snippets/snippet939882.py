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


def __init__(self, args):
    self.args = args
    self.ok = True
    self.log = torch.Tensor()
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    if (args.load == '.'):
        if (args.save == '.'):
            args.save = now
        self.dir = ('../experiment/' + args.save)
    else:
        self.dir = ('../experiment/' + args.load)
        if (not os.path.exists(self.dir)):
            args.load = '.'
        else:
            self.log = torch.load((self.dir + '/psnr_log.pt'))
            print('Continue from epoch {}...'.format(len(self.log)))
    if args.reset:
        os.system(('rm -rf ' + self.dir))
        args.load = '.'

    def _make_dir(path):
        if (not os.path.exists(path)):
            os.makedirs(path)
    _make_dir(self.dir)
    _make_dir((self.dir + '/results'))
    open_type = ('a' if os.path.exists((self.dir + '/log.txt')) else 'w')
    self.log_file = open((self.dir + '/log.txt'), open_type)
    with open((self.dir + '/config.txt'), open_type) as f:
        f.write((now + '\n\n'))
        for arg in vars(args):
            f.write('{}: {}\n'.format(arg, getattr(args, arg)))
        f.write('\n')
