import numpy as np
import tensorflow as tf
from random import shuffle
from collections import namedtuple
from module import *
from ops import *
from utils import *
from glob import glob


def load(self, checkpoint_dir):
    print(' [*] Reading checkpoint...')
    model_dir = 'classifier_{}2{}_{}_{}'.format(self.dataset_A_dir, self.dataset_B_dir, self.now_datetime, str(self.sigma_c))
    checkpoint_dir = os.path.join(checkpoint_dir, model_dir)
    ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
    if (ckpt and ckpt.model_checkpoint_path):
        ckpt_name = os.path.basename(ckpt.model_checkpoint_path)
        self.saver.restore(self.sess, os.path.join(checkpoint_dir, ckpt_name))
        return True
    else:
        return False
