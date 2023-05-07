import argparse
import copy
from datetime import datetime
from enum import Enum
import glob
import importlib
import json
import logging
import math
import numpy as np
import os
import pickle
from pointset import PointSet
import pprint
from queue import Queue
import subprocess
import sys
import tempfile
import tensorflow as tf
import threading
import provider
import tf_util
import pc_util


def pre_processor(files, input_queue):
    for file in files:
        logging.info('Loading {}'.format(file))
        pset = PointSet(file)
        psets = pset.split()
        num_batches = int(math.ceil(((1.0 * len(psets)) / BATCH_SIZE)))
        data = []
        for batch_idx in range(num_batches):
            start_idx = (batch_idx * BATCH_SIZE)
            end_idx = ((batch_idx + 1) * BATCH_SIZE)
            for k in range(FLAGS.n_angles):
                (batch_raw, batch_data) = get_batch(psets, start_idx, end_idx)
                if (k == 0):
                    aug_data = batch_data
                else:
                    ang = ((((1.0 * k) / (1.0 * FLAGS.n_angles)) * 2) * np.pi)
                    if FLAGS.extra_dims:
                        aug_data = np.concatenate((provider.rotate_point_cloud_z(batch_data[(:, :, 0:3)], angle=ang), batch_data[(:, :, 3:)]), axis=2)
                    else:
                        aug_data = provider.rotate_point_cloud_z(batch_data)
                data.append((batch_raw, aug_data))
        logging.debug('Adding {} to queue'.format(file))
        input_queue.put((pset, data))
        logging.debug('Added {} to queue'.format(file))
    logging.info('Pre-processing finished')
    input_queue.put(None)
    logging.debug('Pre-processing thread finished')
