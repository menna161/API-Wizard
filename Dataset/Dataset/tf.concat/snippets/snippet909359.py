import tensorflow as tf
import numpy as np
from .utils import layer
import time


def __init__(self, sess, env, batch_size, layer_number, FLAGS, learning_rate=0.001, tau=0.05, imit_batch_size=32, imit_learning_rate=0.001, imit_ratio=1):
    self.sess = sess
    self.imit_batch_size = imit_batch_size
    self.imit_init_ratio = imit_ratio
    self.imit_ratio = imit_ratio
    self.FLAGS = FLAGS
    if (layer_number == 0):
        self.action_space_bounds = env.action_bounds
        self.action_offset = env.action_offset
    else:
        self.action_space_bounds = env.subgoal_bounds_symmetric
        self.action_offset = env.subgoal_bounds_offset
    if (layer_number == 0):
        self.action_space_size = env.action_dim
    else:
        self.action_space_size = env.subgoal_dim
    self.actor_name = ('actor_' + str(layer_number))
    if (FLAGS.threadings > 1):
        self.actor_name += str(time.time())
    if (layer_number == (FLAGS.layers - 1)):
        self.goal_dim = env.end_goal_dim
    else:
        self.goal_dim = env.subgoal_dim
    self.state_dim = env.state_dim
    self.learning_rate = learning_rate
    self.tau = tau
    self.batch_size = batch_size
    self.state_ph = tf.placeholder(tf.float32, shape=(None, self.state_dim))
    self.goal_ph = tf.placeholder(tf.float32, shape=(None, self.goal_dim))
    self.features_ph = tf.concat([self.state_ph, self.goal_ph], axis=1)
    self.infer = self.create_nn(self.features_ph, self.actor_name)
    self.weights = [v for v in tf.trainable_variables() if (self.actor_name in v.op.name)]
    self.target = self.create_nn(self.features_ph, name=(self.actor_name + '_target'))
    self.target_weights = [v for v in tf.trainable_variables() if (self.actor_name in v.op.name)][len(self.weights):]
    self.update_target_weights = [self.target_weights[i].assign((tf.multiply(self.weights[i], self.tau) + tf.multiply(self.target_weights[i], (1.0 - self.tau)))) for i in range(len(self.target_weights))]
    self.action_derivs = tf.placeholder(tf.float32, shape=(None, self.action_space_size))
    self.unnormalized_actor_gradients = tf.gradients(self.infer, self.weights, (- self.action_derivs))
    self.policy_gradient = list(map((lambda x: tf.div(x, self.batch_size)), self.unnormalized_actor_gradients))
    self.train = tf.train.AdamOptimizer(learning_rate).apply_gradients(zip(self.policy_gradient, self.weights))
    if FLAGS.imitation:
        self.demo_action = tf.placeholder(tf.float32, shape=(None, self.action_space_size))
        self.imit_loss = tf.multiply(self.imit_ratio, tf.reduce_mean(tf.square((self.infer - self.demo_action))))
        self.imit_train = tf.train.AdamOptimizer(imit_learning_rate).minimize(self.imit_loss)
