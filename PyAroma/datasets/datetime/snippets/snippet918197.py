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


def print_to_log_file(self, *args, also_print_to_console=True, add_timestamp=True):
    timestamp = time()
    dt_object = datetime.fromtimestamp(timestamp)
    if add_timestamp:
        args = (('%s:' % dt_object), *args)
    if (self.log_file is None):
        maybe_mkdir_p(self.output_folder)
        timestamp = datetime.now()
        self.log_file = join(self.output_folder, ('training_log_%d_%d_%d_%02.0d_%02.0d_%02.0d.txt' % (timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second)))
        with open(self.log_file, 'w') as f:
            f.write('Starting... \n')
    successful = False
    max_attempts = 5
    ctr = 0
    while ((not successful) and (ctr < max_attempts)):
        try:
            with open(self.log_file, 'a+') as f:
                for a in args:
                    f.write(str(a))
                    f.write(' ')
                f.write('\n')
            successful = True
        except IOError:
            print(('%s: failed to log: ' % datetime.fromtimestamp(timestamp)), sys.exc_info())
            sleep(0.5)
            ctr += 1
    if also_print_to_console:
        print(*args)
