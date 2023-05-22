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


def embedding_layer(self):
    with tf.name_scope('encoder_inputs'):
        self.encoder_embeddings = tf.Variable(initial_value=np.array(self.encoder_embeddings_matrix, dtype=np.float32), dtype=tf.float32, trainable=False)
        self.enc_embed_input = tf.nn.embedding_lookup(self.encoder_embeddings, self.input_data)
        self.enc_embed_input = self.enc_embed_input[(:, :tf.reduce_max(self.source_sentence_length), :)]
    with tf.name_scope('decoder_inputs'):
        self.decoder_embeddings = tf.Variable(initial_value=np.array(self.decoder_embeddings_matrix, dtype=np.float32), dtype=tf.float32, trainable=False)
        keep = tf.where((tf.random_uniform([self.batch_size, self.decoder_num_tokens]) < self.word_dropout_keep_prob), tf.fill([self.batch_size, self.decoder_num_tokens], True), tf.fill([self.batch_size, self.decoder_num_tokens], False))
        ending = (tf.cast(keep, dtype=tf.int32) * self.target_data)
        ending = tf.strided_slice(ending, [0, 0], [self.batch_size, (- 1)], [1, 1], name='slice_input')
        self.dec_input = tf.concat([tf.fill([self.batch_size, 1], self.decoder_word_index['GO']), ending], 1, name='dec_input')
        self.dec_embed_input = tf.nn.embedding_lookup(self.decoder_embeddings, self.dec_input)
        self.max_tar_len = tf.reduce_max(self.target_sentence_length)
        self.dec_embed_input = self.dec_embed_input[(:, :self.max_tar_len, :)]
