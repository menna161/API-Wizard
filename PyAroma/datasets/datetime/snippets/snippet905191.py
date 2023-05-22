from model import Model
import tensorflow as tf
import datetime
from utils import data_utils, prior_utils
import numpy as np
import config


def train_on_batch(self, sess, input_words, input_textlen, input_mentions, input_mentionlen, input_positions, input_labels):
    feed = self.create_feed_dict(input_words, input_textlen, input_mentions, input_mentionlen, input_positions, input_labels, True, self.dense_keep_prob, self.rnn_keep_prob)
    (_, step, loss, pacc, eacc) = sess.run([self.train_op, self.global_step, self.loss, self.partial_accuracy, self.exact_accuracy], feed_dict=feed)
    time_str = datetime.datetime.now().isoformat()
    print('{}: step {}, loss {:g} pacc {:g} eacc {:g}'.format(time_str, step, loss, pacc, eacc))
