import numpy as np
import tensorflow as tf
from random import shuffle
from collections import namedtuple
from module import *
from ops import *
from utils import *
from glob import glob


def save(self, checkpoint_dir, step):
    model_name = 'classifier.model'
    model_dir = 'classifier_{}2{}_{}_{}'.format(self.dataset_A_dir, self.dataset_B_dir, self.now_datetime, str(self.sigma_c))
    checkpoint_dir = os.path.join(checkpoint_dir, model_dir)
    if (not os.path.exists(checkpoint_dir)):
        os.makedirs(checkpoint_dir)
    self.saver.save(self.sess, os.path.join(checkpoint_dir, model_name), global_step=step)
