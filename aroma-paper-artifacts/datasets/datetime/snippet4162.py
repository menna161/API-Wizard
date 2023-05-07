from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import logging
import multiprocessing
import sys
import time
from datetime import datetime
from multiprocessing import Process, Queue
import pandas as pd
import tensorflow as tf


def writing_loop():
    '\n            function to be executed within the single writing process.\n\n            Args:\n              out_queue: the queue used to store serialized tf.Examples as strings.\n              out_file: string, path to the TFRecord file for transformed tf.Example protos.\n            '
    options = tf.io.TFRecordOptions(compression_type='GZIP')
    writer = tf.io.TFRecordWriter(out_file, options=(options if self.gzip else None))
    sample_count = 0
    while True:
        raw_example = self.out_queue.get()
        logging.debug('writing_loop raw_example:{}'.format(raw_example))
        if isinstance(raw_example, str):
            break
        writer.write(raw_example)
        sample_count += 1
        if (not (sample_count % 1000)):
            logging.info(('%s Processed %d examples' % (datetime.now(), (sample_count * prebatch))))
            sys.stdout.flush()
    writer.close()
    logging.info(('%s >>>> Processed %d examples <<<<' % (datetime.now(), (sample_count * prebatch))))
    self.sample_cnt = sample_count
    sys.stdout.flush()
