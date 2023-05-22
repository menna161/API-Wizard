import tensorflow as tf
import numpy as np
import math


def __init__(self, sigma_prior, n_in, init_rho=None, momentum=0.99, beta_initializer=tf.zeros_initializer(), gamma_initializer=tf.ones_initializer(), name='batch_norm_bayes', reuse=None):
    self.momentum = momentum
    self.sigma_prior = sigma_prior
    with tf.variable_scope(name, reuse=reuse):
        self.moving_mean = tf.get_variable('moving_mean', [n_in], initializer=tf.zeros_initializer(), trainable=False)
        self.moving_var = tf.get_variable('moving_var', [n_in], initializer=tf.ones_initializer(), trainable=False)
        self.mu_gamma = tf.get_variable('mu_gamma', shape=[n_in], initializer=tf.initializers.random_uniform(0, 1))
        self.mu_beta = tf.get_variable('mu_beta', shape=[n_in], initializer=tf.zeros_initializer())
        self.epsilon_gamma = tf.random.normal(shape=[n_in], mean=0.0, stddev=1.0)
        self.epsilon_beta = tf.random.normal(shape=[n_in], mean=0.0, stddev=1.0)
        if (init_rho is None):
            self.rho_gamma = tf.get_variable('rho_gamma', shape=[n_in])
            self.rho_beta = tf.get_variable('rho_beta', shape=[n_in])
        else:
            self.rho_gamma = tf.get_variable('rho_gamma', shape=[n_in], initializer=tf.constant_initializer(value=init_rho))
            self.rho_beta = tf.get_variable('rho_beta', shape=[n_in], initializer=tf.constant_initializer(value=init_rho))
        self.sigma_gamma = softplus(self.rho_gamma)
        self.sigma_beta = softplus(self.rho_beta)
