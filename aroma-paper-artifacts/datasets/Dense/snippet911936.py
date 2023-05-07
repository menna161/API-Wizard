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
        self.z_tilda = Dense(self.latent_dim, name='z_tilda')(self.h_N)
