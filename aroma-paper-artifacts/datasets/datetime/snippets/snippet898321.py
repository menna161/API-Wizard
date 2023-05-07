from model import Model
import tensorflow as tf
import datetime
from utils import data_utils
import numpy as np
import config
from sklearn.metrics import average_precision_score


def predict(self, sess, test):
    batches = data_utils.batch_iter(test, self.batch_size, 1, shuffle=False)
    all_probs = np.zeros((0, (self.num_classes - 1)))
    all_labels = []
    total_cnt = 0
    total_size = 0
    for batch in batches:
        (words_batch, textlen_batch, positions_batch, labels_batch) = zip(*batch)
        feed = self.create_feed_dict(words_batch, textlen_batch, positions_batch, labels_batch)
        (loss, probs, size, cnt) = sess.run([self.loss, self.probs, self.valid_size, self.correct_num], feed_dict=feed)
        total_cnt += cnt
        total_size += size
        all_probs = np.concatenate((all_probs, probs[(:, 1:)]))
        for l in labels_batch:
            tmp = np.zeros((self.num_classes - 1))
            if (l > 0):
                tmp[(l - 1)] = 1.0
            all_labels.append(tmp)
    all_probs = np.reshape(all_probs, (- 1))
    all_labels = np.reshape(np.array(all_labels), (- 1))
    return (all_labels, all_probs, (total_cnt / total_size))
