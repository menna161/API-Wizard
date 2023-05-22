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


def _store_ping(self, overwrite=False):
    if (not self._logdir):
        return
    try:
        (last_worker, _) = self._read_ping()
        if (last_worker is None):
            self._logger.info("Create directory '{}'.".format(self._logdir))
            tf.gfile.MakeDirs(self._logdir)
        elif ((last_worker != self._worker_name) and (not overwrite)):
            raise WorkerConflict
        with tf.gfile.Open(os.path.join(self._logdir, 'PING'), 'wb') as file_:
            pickle.dump((self._worker_name, datetime.datetime.utcnow()), file_)
    except (EOFError, IOError, tf.errors.NotFoundError):
        raise WorkerConflict
