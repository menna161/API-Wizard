from data import *
from utils.augmentations import SSDAugmentation
from layers.modules import MultiBoxLoss
from ssd import build_ssd
import os
import sys
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn
import torch.nn.init as init
import torch.utils.data as data
import argparse
from utils import helpers
import logging
import time
import datetime
from torchviz import make_dot
import visdom

if (__name__ == '__main__'):
    args = init_args()
    start = time.time()
    try:
        filepath = os.path.join(args.log_dir, (((args.exp_name + '_') + str(round(time.time()))) + '.log'))
        print(('Logging to ' + filepath))
        logging.basicConfig(filename=filepath, filemode='w', format='%(process)d - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
        train(args)
    except Exception as e:
        logging.error('Exception occurred', exc_info=True)
    end = time.time()
    logging.debug(('Total time taken ' + str(datetime.timedelta(seconds=(end - start)))))
    logging.debug('Training done!')
