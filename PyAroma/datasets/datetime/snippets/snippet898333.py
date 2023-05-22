from model import Model
import tensorflow as tf
import datetime
from utils import data_utils
import numpy as np
import config
from sklearn.metrics import average_precision_score


def validation(self, sess, valid):
    batches = data_utils.batch_iter(valid, self.batch_size, 1, shuffle=False)
    total_loss = 0.0
    total_len = 0
    total_cnt = 0
    total_size = 0
    all_probs = np.zeros((0, (self.num_classes - 1)))
    all_labels = []
    for batch in batches:
        (words_batch, textlen_batch, positions_batch, heads_batch, tails_batch, labels_batch) = zip(*batch)
        feed = self.create_feed_dict(words_batch, textlen_batch, positions_batch, heads_batch, tails_batch, labels_batch)
        (loss, size, cnt, probs) = sess.run([self.loss, self.valid_size, self.correct_num, self.probs], feed_dict=feed)
        total_loss += (loss * len(labels_batch))
        total_len += len(labels_batch)
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
    average_precision = average_precision_score(all_labels, all_probs)
    time_str = datetime.datetime.now().isoformat()
    print('{}: loss {:g} acc {:g} ap {:g}'.format(time_str, (total_loss / total_len), (total_cnt / total_size), average_precision))
    return ((total_loss / total_len), (total_cnt / total_size), average_precision)
