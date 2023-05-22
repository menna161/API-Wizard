from __future__ import print_function
import os
import argparse
import torch.backends.cudnn as cudnn
from ssd import build_ssd
from utils import draw_boxes, helpers, save_boxes
import logging
import time
import datetime
from torch.autograd import Variable
from torchvision import datasets, transforms
from torch.utils.data import Dataset, DataLoader
from data import *
import shutil
import torch.nn as nn

if (__name__ == '__main__'):
    args = parse_args()
    start = time.time()
    try:
        filepath = os.path.join(args.log_dir, (((args.exp_name + '_') + str(round(time.time()))) + '.log'))
        print(('Logging to ' + filepath))
        logging.basicConfig(filename=filepath, filemode='w', format='%(process)d - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
        test_gtdb(args)
    except Exception as e:
        logging.error('Exception occurred', exc_info=True)
    end = time.time()
    logging.debug(('Toal time taken ' + str(datetime.timedelta(seconds=(end - start)))))
    logging.debug('Testing done!')
