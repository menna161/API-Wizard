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


def build_encoder(self):
    with tf.name_scope('encode'):
        for layer in range(self.num_layers):
            with tf.variable_scope('encoder_{}'.format((layer + 1))):
                cell_fw = tf.contrib.rnn.LayerNormBasicLSTMCell(self.lstm_hidden_units)
                cell_fw = tf.contrib.rnn.DropoutWrapper(cell_fw, input_keep_prob=self.keep_prob)
                cell_bw = tf.contrib.rnn.LayerNormBasicLSTMCell(self.lstm_hidden_units)
                cell_bw = tf.contrib.rnn.DropoutWrapper(cell_bw, input_keep_prob=self.keep_prob)
                (self.enc_output, self.enc_state) = tf.nn.bidirectional_dynamic_rnn(cell_fw, cell_bw, self.enc_embed_input, self.source_sentence_length, dtype=tf.float32)
        self.h_N = tf.concat([self.enc_state[0][1], self.enc_state[1][1]], axis=(- 1), name='h_N')
        self.enc_outputs = tf.concat([self.enc_output[0], self.enc_output[1]], axis=(- 1), name='encoder_outputs')
