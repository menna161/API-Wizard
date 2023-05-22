from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import datetime
import itertools
import os
import pickle
import six
import sys
import threading
import time
import traceback
import uuid
import numpy as np
import tensorflow as tf


def _read_ping(self):
    if (not tf.gfile.Exists(os.path.join(self._logdir, 'PING'))):
        return (None, None)
    try:
        with tf.gfile.Open(os.path.join(self._logdir, 'PING'), 'rb') as file_:
            (last_worker, last_ping) = pickle.load(file_)
        duration = (datetime.datetime.utcnow() - last_ping).total_seconds()
        return (last_worker, duration)
    except (EOFError, IOError, tf.errors.NotFoundError):
        raise WorkerConflict
