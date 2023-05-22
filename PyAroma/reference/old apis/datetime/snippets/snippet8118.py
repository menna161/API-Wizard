import argparse
import os
import datetime
import re
from .model import model_fn, ALLOWED_NETWORK_NAMES
from . import dataset
import tensorflow as tf
from tensorflow.contrib.training.python.training import hparam


def get_model_name(hparams):
    '\n    Generate a (hopefully) unique name for the model based on the hyperparameters and datetime information.\n    '
    skipped = {'job_dir', 'dataset_dir', 'verbosity', 'threads'}
    filtered_hparams = [(key, value) for (key, value) in sorted(hparams.values().items()) if (key not in skipped)]
    hyperparams_str = ','.join(('{}={}'.format(re.sub('(.)[^_]*_?', '\\1', key), value) for (key, value) in filtered_hparams))
    model_name = '{}-{}-{}'.format(os.path.basename(__file__), datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'), hyperparams_str)
    return model_name
