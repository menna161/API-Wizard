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
from decoder import basic_decoder


def embedding_layer(self):
    with tf.name_scope('word_embeddings'):
        self.embeddings = tf.Variable(initial_value=np.array(self.embeddings_matrix, dtype=np.float32), dtype=tf.float32, trainable=False)
        self.enc_embed_input = tf.nn.embedding_lookup(self.embeddings, self.input_data)
        self.enc_embed_input = self.enc_embed_input[(:, :tf.reduce_max(self.source_sentence_length), :)]
        with tf.name_scope('decoder_inputs'):
            shifted = self.target_data[(:, :(- 1))]
            self.dec_input = tf.concat([tf.fill([self.batch_size, 1], self.word_index['GO']), shifted], 1, name='dec_input')
            self.dec_embed_input = tf.nn.embedding_lookup(self.embeddings, self.dec_input)
            self.max_tar_len = tf.reduce_max(self.target_sentence_length)
            self.dec_embed_input = self.dec_embed_input[(:, :self.max_tar_len, :)]
