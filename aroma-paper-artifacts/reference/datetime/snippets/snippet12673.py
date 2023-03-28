import tensorflow as tf
import os
import time
import numpy as np
import argparse


def create_folders(prefix, **kwargs):
    datetime = time.strftime('%d%m%Y_%H%M%S')
    hyperparameters = ''.join((((('_' + str(key)) + '_') + str(value)) for (key, value) in sorted(kwargs.items())))
    experiment_id = ((((prefix + '_') + datetime) + '_') + hyperparameters)
    ckpt_path = './checkpoint'
    log_path = './log'
    os.makedirs(os.path.join(ckpt_path, kwargs['dset'], experiment_id))
    os.makedirs(os.path.join(log_path, kwargs['dset'], experiment_id))
    return experiment_id
