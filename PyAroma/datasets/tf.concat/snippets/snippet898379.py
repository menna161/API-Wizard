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
        E = tf.Variable(self.entity_embedding, dtype=tf.float32, name='E')
        self.e1 = tf.nn.embedding_lookup(E, self.input_heads)
        self.e2 = tf.nn.embedding_lookup(E, self.input_tails)
        self.var_list1.append(E)
