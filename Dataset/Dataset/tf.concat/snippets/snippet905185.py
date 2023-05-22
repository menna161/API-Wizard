from model import Model
import tensorflow as tf
import datetime
from utils import data_utils, prior_utils
import numpy as np
import config


def add_embedding(self):
    with tf.device('/cpu:0'), tf.name_scope('word_embedding'):
        W = tf.Variable(self.pretrained_embedding, trainable=False, dtype=tf.float32, name='W')
        self.embedded_words = tf.nn.embedding_lookup(W, self.input_words)
        self.embedded_mentions = tf.nn.embedding_lookup(W, self.input_mentions)
        self.mention_embedding = tf.divide(tf.reduce_sum(tf.nn.embedding_lookup(W, self.mention), axis=1), self.mentionlen)
    with tf.device('/cpu:0'), tf.name_scope('position_embedding'):
        W = tf.Variable(self.wpe, trainable=False, dtype=tf.float32, name='W')
        self.wpe_chars = tf.nn.embedding_lookup(W, self.input_positions)
    self.input_sentences = tf.concat([self.embedded_words, self.wpe_chars], 2)
