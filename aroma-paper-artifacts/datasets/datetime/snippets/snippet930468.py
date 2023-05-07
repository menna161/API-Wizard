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


def _gather_run_info(model_name, dataset_name, run_params, test_id):
    'Collect the benchmark run information for the local environment.'
    run_info = {'model_name': model_name, 'dataset': {'name': dataset_name}, 'machine_config': {}, 'test_id': test_id, 'run_date': datetime.datetime.utcnow().strftime(_DATE_TIME_FORMAT_PATTERN)}
    _collect_tensorflow_info(run_info)
    _collect_tensorflow_environment_variables(run_info)
    _collect_run_params(run_info, run_params)
    _collect_cpu_info(run_info)
    _collect_gpu_info(run_info)
    _collect_memory_info(run_info)
    _collect_test_environment(run_info)
    return run_info
