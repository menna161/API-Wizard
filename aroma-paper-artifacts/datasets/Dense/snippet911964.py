from pathsetup import run_path_setup
import time
import pickle
import tensorflow as tf
import numpy as np
import utils
import gl
import os
from tqdm import tqdm
from nltk.tokenize import word_tokenize
from tensorflow.python.layers.core import Dense
from snli.decoder import basic_decoder
from scipy.stats import logistic


def build_latent_space(self):
    with tf.name_scope('latent_space'):
        self.z_mean = Dense(self.latent_dim, name='z_mean')(self.h_N)
        self.z_log_sigma = Dense(self.latent_dim, name='z_log_sigma')(self.h_N)
        self.z_tilda = tf.identity(self.sample_z_tilda_from_posterior(), name='z_tilda')
