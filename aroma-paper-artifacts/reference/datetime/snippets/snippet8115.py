import argparse
import os
import datetime
import re
import tqdm
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.contrib.training.python.training import hparam
from .model import model_fn
from .task import SEED
from . import dataset


def get_model_name(hparams):
    skipped = {'job_dir', 'dataset_dir', 'verbosity', 'threads'}
    filtered_hparams = [(key, value) for (key, value) in sorted(hparams.values().items()) if (key not in skipped)]
    model_name = '{}-{}-{}'.format(os.path.basename(__file__), datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'), ','.join(('{}={}'.format(re.sub('(.)[^_]*_?', '\\1', key), value) for (key, value) in filtered_hparams)))
    return model_name
