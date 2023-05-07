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


def load(self, checkpoint_dir):
    print(' [*] Reading checkpoint...')
    model_dir = '{}2{}_{}_{}_{}'.format(self.dataset_A_dir, self.dataset_B_dir, self.now_datetime, self.model, self.sigma_d)
    checkpoint_dir = os.path.join(checkpoint_dir, model_dir)
    ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
    if (ckpt and ckpt.model_checkpoint_path):
        ckpt_name = os.path.basename(ckpt.model_checkpoint_path)
        self.saver.restore(self.sess, os.path.join(checkpoint_dir, ckpt_name))
        return True
    else:
        return False
