from __future__ import print_function
import random as rand
import csv
import operator
import gc
import os
from datetime import datetime
from keras.callbacks import EarlyStopping
from keras.models import load_model
import keras.backend as K
from sklearn.metrics import log_loss
import numpy as np
import tensorflow as tf


def __init__(self, genome_handler, data_path=''):
    '\n        Initialize a DEvol object which carries out the training and evaluation\n        of a genetic search.\n\n        Args:\n            genome_handler (GenomeHandler): the genome handler object defining\n                    the restrictions for the architecture search space\n            data_path (str): the file which the genome encodings and metric data\n                    will be stored in\n        '
    self.genome_handler = genome_handler
    self.datafile = (data_path or (datetime.now().ctime() + '.csv'))
    self._bssf = (- 1)
    if (os.path.isfile(data_path) and (os.stat(data_path).st_size > 1)):
        raise ValueError(('Non-empty file %s already exists. Please changefile path to prevent overwritten genome data.' % data_path))
    print('Genome encoding and metric data stored at', self.datafile, '\n')
    with open(self.datafile, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        metric_cols = ['Val Loss', 'Val Accuracy']
        genome = (genome_handler.genome_representation() + metric_cols)
        writer.writerow(genome)
