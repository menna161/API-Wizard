from model import Model
import tensorflow as tf
import datetime
from utils import data_utils
import numpy as np
import config
from sklearn.metrics import average_precision_score


def add_embedding(self):
    with tf.device('/cpu:0'), tf.name_scope('word_embedding'):
        W = tf.Variable(self.pretrained_embedding, trainable=False, dtype=tf.float32, name='W')
        self.embedded_words = tf.nn.embedding_lookup(W, self.input_words_flatten)
    with tf.device('/cpu:0'), tf.name_scope('position_embedding'):
        W = tf.Variable(self.wpe, trainable=False, dtype=tf.float32, name='W')
        self.wpe_chars = tf.nn.embedding_lookup(W, self.input_positions_flatten)
    self.input_sentences = tf.concat(([self.embedded_words] + tf.unstack(self.wpe_chars, axis=1)), 2)
    with tf.device('/cpu:0'), tf.name_scope('entity_embedding'):
        E1 = tf.Variable(self.entity_embedding1, dtype=tf.float32, name='E1')
        E2 = tf.Variable(self.entity_embedding2, dtype=tf.float32, name='E2')
        self.e1_1 = tf.tanh(tf.nn.embedding_lookup(E1, self.input_heads))
        self.e1_2 = tf.tanh(tf.nn.embedding_lookup(E2, self.input_heads))
        self.e2_1 = tf.tanh(tf.nn.embedding_lookup(E1, self.input_tails))
        self.e2_2 = tf.tanh(tf.nn.embedding_lookup(E2, self.input_tails))
        self.var_list1.append(E1)
        self.var_list1.append(E2)
