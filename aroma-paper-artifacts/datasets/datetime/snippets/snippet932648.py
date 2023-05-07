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


def __init__(self, sess, args):
    self.sess = sess
    self.batch_size = args.batch_size
    self.image_size = args.fine_size
    self.time_step = args.time_step
    self.pitch_range = args.pitch_range
    self.input_c_dim = args.input_nc
    self.output_c_dim = args.output_nc
    self.L1_lambda = args.L1_lambda
    self.gamma = args.gamma
    self.sigma_d = args.sigma_d
    self.dataset_dir = args.dataset_dir
    self.dataset_A_dir = args.dataset_A_dir
    self.dataset_B_dir = args.dataset_B_dir
    self.sample_dir = args.sample_dir
    self.model = args.model
    self.discriminator = discriminator
    self.generator = generator_resnet
    self.criterionGAN = mae_criterion
    OPTIONS = namedtuple('OPTIONS', 'batch_size image_size gf_dim df_dim output_c_dim is_training')
    self.options = OPTIONS._make((args.batch_size, args.fine_size, args.ngf, args.ndf, args.output_nc, (args.phase == 'train')))
    self._build_model()
    self.saver = tf.train.Saver(max_to_keep=30)
    self.now_datetime = get_now_datetime()
    self.pool = ImagePool(args.max_size)
