from model import Model
import tensorflow as tf
import datetime
from utils import data_utils
import numpy as np
import config
from sklearn.metrics import average_precision_score


def train_on_batch(self, sess, input_words, input_textlen, input_positions, input_heads, input_tails, input_labels):
    feed = self.create_feed_dict(input_words, input_textlen, input_positions, input_heads, input_tails, input_labels, True, self.dense_keep_prob, self.rnn_keep_prob)
    (_, step, loss, size, cnt) = sess.run([self.train_op, self.global_step, self.loss, self.valid_size, self.correct_num], feed_dict=feed)
    acc = 0.0
    if (size > 0):
        acc = (cnt / size)
    time_str = datetime.datetime.now().isoformat()
    print('{}: step {}, loss {:g}, acc {:g}'.format(time_str, step, loss, acc))
