from model import Model
import tensorflow as tf
import datetime
from utils import data_utils, prior_utils
import numpy as np
import config


def evaluation_on_dev(self, sess, dev):
    batches = data_utils.batch_iter(dev, self.batch_size, 1, shuffle=False)
    total_loss = 0.0
    total_pacc = 0.0
    total_eacc = 0.0
    total_len = 0
    for batch in batches:
        (words_batch, textlen_batch, mentions_batch, mentionlen_batch, positions_batch, labels_batch) = zip(*batch)
        feed = self.create_feed_dict(words_batch, textlen_batch, mentions_batch, mentionlen_batch, positions_batch, labels_batch)
        (loss, pacc, eacc) = sess.run([self.loss, self.partial_accuracy, self.exact_accuracy], feed_dict=feed)
        total_loss += (loss * len(labels_batch))
        total_pacc += (pacc * len(labels_batch))
        total_eacc += (eacc * len(labels_batch))
        total_len += len(labels_batch)
    time_str = datetime.datetime.now().isoformat()
    print('{}: loss {:g} partial acc {:g} exact acc {:g}'.format(time_str, (total_loss / total_len), (total_pacc / total_len), (total_eacc / total_len)))
    return ((total_loss / total_len), (total_pacc / total_len), (total_eacc / total_len))
