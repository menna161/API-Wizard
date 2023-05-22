import numpy as np
import tensorflow as tf
from random import shuffle
from collections import namedtuple
from module import *
from ops import *
from utils import *
from glob import glob


def __init__(self, sess, args):
    self.sess = sess
    self.dataset_dir = args.dataset_dir
    self.dataset_A_dir = args.dataset_A_dir
    self.dataset_B_dir = args.dataset_B_dir
    self.sample_dir = args.sample_dir
    self.batch_size = args.batch_size
    self.image_size = args.fine_size
    self.time_step = args.time_step
    self.pitch_range = args.pitch_range
    self.input_c_dim = args.input_nc
    self.sigma_c = args.sigma_c
    self.sigma_d = args.sigma_d
    self.model = args.model
    self.generator = generator_resnet
    self.discriminator = discriminator_classifier
    self.criterionGAN = softmax_criterion
    OPTIONS = namedtuple('OPTIONS', 'batch_size image_size gf_dim df_dim output_c_dim is_training')
    self.options = OPTIONS._make((args.batch_size, args.fine_size, args.ngf, args.ndf, args.output_nc, (args.phase == 'train')))
    self._build_model()
    self.now_datetime = get_now_datetime()
    self.saver = tf.train.Saver()
