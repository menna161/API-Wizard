from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import datetime
import operator
import os
import tensorflow as tf
import thumt.utils.bleu as bleu


def _save_log(filename, result):
    (metric, global_step, score) = result
    with open(filename, 'a') as fd:
        time = datetime.datetime.now()
        msg = ('%s: %s at step %d: %f\n' % (time, metric, global_step, score))
        fd.write(msg)
