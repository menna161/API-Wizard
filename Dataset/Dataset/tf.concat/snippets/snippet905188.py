from model import Model
import tensorflow as tf
import datetime
from utils import data_utils, prior_utils
import numpy as np
import config


def add_prediction_op(self):
    self.add_embedding()
    with tf.name_scope('sentence_repr'):
        attention_w = tf.get_variable('attention_w', [self.state_size, 1])
        cell_forward = tf.contrib.rnn.LSTMCell(self.state_size)
        cell_backward = tf.contrib.rnn.LSTMCell(self.state_size)
        cell_forward = tf.contrib.rnn.DropoutWrapper(cell_forward, input_keep_prob=self.dense_dropout, output_keep_prob=self.rnn_dropout, seed=config.RANDOM_SEED)
        cell_backward = tf.contrib.rnn.DropoutWrapper(cell_backward, input_keep_prob=self.dense_dropout, output_keep_prob=self.rnn_dropout, seed=config.RANDOM_SEED)
        (outputs, states) = tf.nn.bidirectional_dynamic_rnn(cell_forward, cell_backward, self.input_sentences, sequence_length=self.input_textlen, dtype=tf.float32)
        outputs_added = tf.nn.tanh(tf.add(outputs[0], outputs[1]))
        alpha = tf.nn.softmax(tf.reshape(tf.matmul(tf.reshape(outputs_added, [(- 1), self.state_size]), attention_w), [(- 1), self.sequence_length]))
        alpha = tf.expand_dims(alpha, 1)
        self.sen_repr = tf.squeeze(tf.matmul(alpha, outputs_added))
    with tf.name_scope('mention_repr'):
        cell = tf.contrib.rnn.LSTMCell(self.state_size)
        cell = tf.contrib.rnn.DropoutWrapper(cell, input_keep_prob=self.dense_dropout, output_keep_prob=self.rnn_dropout, seed=config.RANDOM_SEED)
        (outputs, states) = tf.nn.dynamic_rnn(cell, self.embedded_mentions, sequence_length=self.input_mentionlen, dtype=tf.float32)
        self.men_repr = self.extract_last_relevant(outputs, self.input_mentionlen)
    self.features = tf.concat([self.sen_repr, self.men_repr, self.mention_embedding], (- 1))
    self.feature_dim = ((self.state_size * 2) + self.embedding_size)
    h_drop = tf.nn.dropout(tf.nn.relu(self.features), self.dense_dropout, seed=config.RANDOM_SEED)
    h_drop.set_shape([None, self.feature_dim])
    h_output = tf.layers.batch_normalization(h_drop, training=self.phase)
    for i in range(self.hidden_layers):
        h_output = self.add_hidden_layer(h_output, i)
    if (self.hidden_layers == 0):
        self.hidden_size = self.feature_dim
    with tf.variable_scope('output'):
        W = tf.get_variable('W', shape=[self.hidden_size, self.num_classes], initializer=tf.contrib.layers.xavier_initializer(seed=config.RANDOM_SEED))
        b = tf.get_variable('b', shape=[self.num_classes], initializer=tf.contrib.layers.xavier_initializer(seed=config.RANDOM_SEED))
        self.scores = tf.nn.xw_plus_b(h_output, W, b, name='scores')
        self.proba = tf.nn.softmax(self.scores, name='proba')
        self.adjusted_proba = tf.matmul(self.proba, self.tune)
        self.adjusted_proba = tf.clip_by_value(self.adjusted_proba, 1e-10, 1.0)
        self.predictions = tf.argmax(self.adjusted_proba, 1, name='predictions')
