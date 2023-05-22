import tensorflow as tf
import numpy as np
from .utils import create_nn


def _build_net(self):
    self.state = tf.placeholder(tf.float32, [None, self.state_dim], name=(self.name + 'state'))
    self.next_state = tf.placeholder(tf.float32, [None, self.state_dim], name=(self.name + 'next_state'))
    self.action = tf.placeholder(tf.float32, [None, self.action_dim], name=(self.name + 'action'))
    self.input = tf.concat((self.state, self.action), axis=(- 1))
    with tf.variable_scope((self.name + 'train_net')):
        l1 = create_nn(self.input, self.input_dim, 64, relu=True, trainable=True, name='l1')
        self.train_net_output = create_nn(l1, 64, self.state_dim, relu=False, trainable=True, name='output')
    self.loss = tf.reduce_mean(tf.squared_difference(self.train_net_output, self.next_state))
    self.intrinsic_reward = tf.reduce_mean(tf.squared_difference(self.train_net_output, self.next_state), axis=(- 1))
    self._train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)
