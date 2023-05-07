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


def __call__(self, dataframe, out_file, prebatch=1, *args, **kwargs):
    '\n        Transforms tablue data in pandas.DataFrame format to tf.Example protos and dump to a TFRecord file.\n            The benefit of doing this is to use existing training and evaluating functionality within tf\n            packages.\n\n        :param dataframe:   intput pd.DataFrame data\n        :param out_file:    output TFRercord file path\n        :param prebatch:    batch size of examples to package into TFRecord file\n        :param args:\n        :param kwargs:\n        :return:\n        '

    def parsing_loop():
        '\n            function to be executed within each parsing process.\n\n            Args:\n              in_queue: the queue used to store avazu data records as strings.\n              out_queue: the queue used to store serialized tf.Examples as strings.\n            '
        while True:
            raw_record = self.in_queue.get()
            if isinstance(raw_record, str):
                break
            features = {}
            for item in raw_record.columns:
                tmp = list(raw_record[item].values)
                if (item in self.CATEGORY_FEATURES):
                    features[item] = self._int64_feature(tmp)
                elif (item in self.VARIABLE_FEATURES):
                    features[item] = self._int64_feature(tmp[0])
                elif (item in self.NUMERICAL_FEATURES):
                    features[item] = self._float_feature(tmp)
                elif (item in self.LABEL):
                    features[item] = self._int64_feature(tmp)
            example = tf.train.Example(features=tf.train.Features(feature=features))
            raw_example = example.SerializeToString()
            self.out_queue.put(raw_example)

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
    start_time = time.time()
    num_parsers = int((multiprocessing.cpu_count() - 1))
    parsers = []
    for i in range(num_parsers):
        p = Process(target=parsing_loop)
        parsers.append(p)
        p.start()
    writer = Process(target=writing_loop)
    writer.start()
    for i in range(0, len(dataframe), prebatch):
        line = dataframe[i:(i + prebatch)]
        if (len(line) < prebatch):
            continue
        self.in_queue.put(line)
    for i in range(num_parsers):
        self.in_queue.put('DONE')
    for i in range(num_parsers):
        parsers[i].join()
    self.out_queue.put('DONE')
    writer.join()
    end_time = time.time()
    total_time = (end_time - start_time)
    logging.warning(('Total time %.2f s, speed %.2f sample/s, total samples %d.' % (total_time, (len(dataframe) / total_time), len(dataframe))))
    logging.info(('%s >>>> END of consuming input file %s <<<<' % (datetime.now(), out_file)))
    sys.stdout.flush()
