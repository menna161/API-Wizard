from __future__ import division
import os
import time
from shutil import copyfile
from glob import glob
import tensorflow as tf
import numpy as np
import config
from collections import namedtuple
from module import *
from utils import *
from ops import *
from metrics import *


def save(self, checkpoint_dir, step):
    model_name = 'cyclegan.model'
    model_dir = '{}2{}_{}_{}_{}'.format(self.dataset_A_dir, self.dataset_B_dir, self.now_datetime, self.model, self.sigma_d)
    checkpoint_dir = os.path.join(checkpoint_dir, model_dir)
    if (not os.path.exists(checkpoint_dir)):
        os.makedirs(checkpoint_dir)
    self.saver.save(self.sess, os.path.join(checkpoint_dir, model_name), global_step=step)
