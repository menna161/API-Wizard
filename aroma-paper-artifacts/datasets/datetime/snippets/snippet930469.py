from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import contextlib
import datetime
import json
import multiprocessing
import numbers
import os
import threading
import uuid
from six.moves import _thread as thread
from absl import flags
import tensorflow as tf
from tensorflow.python.client import device_lib
from official.utils.logs import cloud_lib
import cpuinfo
import psutil
from official.benchmark import benchmark_uploader as bu


def _process_metric_to_json(name, value, unit=None, global_step=None, extras=None):
    'Validate the metric data and generate JSON for insert.'
    if (not isinstance(value, numbers.Number)):
        tf.logging.warning('Metric value to log should be a number. Got %s', type(value))
        return None
    extras = _convert_to_json_dict(extras)
    return {'name': name, 'value': float(value), 'unit': unit, 'global_step': global_step, 'timestamp': datetime.datetime.utcnow().strftime(_DATE_TIME_FORMAT_PATTERN), 'extras': extras}
