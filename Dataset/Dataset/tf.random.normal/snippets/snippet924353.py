import tensorflow as tf
import numpy as np
import math


def __init__(self, sigma_prior, n_in, n_out, kernel_size, init_rho=None, strides=1, padding='VALID', name='conv_bayes', reuse=None):
    self.strides = 1
    self.padding = padding
    self.sigma_prior = sigma_prior
    self.kernel_size = kernel_size
    limit = (1.0 / math.sqrt((n_in * (kernel_size ** 2))))
    with tf.variable_scope(name, reuse=reuse):
        self.mu_w = tf.get_variable('mu_w', shape=[kernel_size, kernel_size, n_in, n_out], initializer=tf.initializers.random_uniform((- limit), limit), dtype=tf.float32)
        self.mu_b = tf.get_variable('mu_b', shape=[n_out], initializer=tf.initializers.random_uniform((- limit), limit), dtype=tf.float32)
        self.epsilon_w = tf.random.normal(shape=[kernel_size, kernel_size, n_in, n_out], mean=0.0, stddev=1.0)
        self.epsilon_b = tf.random.normal(shape=[n_out], mean=0.0, stddev=1.0)
        if (init_rho is None):
            self.rho_w = tf.get_variable('rho_w', shape=[kernel_size, kernel_size, n_in, n_out], dtype=tf.float32)
            self.rho_b = tf.get_variable('rho_b', shape=[n_out], dtype=tf.float32)
        else:
            self.rho_w = tf.get_variable('rho_w', shape=[kernel_size, kernel_size, n_in, n_out], initializer=tf.constant_initializer(value=init_rho), dtype=tf.float32)
            self.rho_b = tf.get_variable('rho_b', shape=[n_out], initializer=tf.constant_initializer(value=init_rho), dtype=tf.float32)
        self.sigma_w = softplus(self.rho_w)
        self.sigma_b = softplus(self.rho_b)
