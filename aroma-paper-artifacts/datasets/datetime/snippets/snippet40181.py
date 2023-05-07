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


def post_processor(output_queue):
    while True:
        out_data = output_queue.get()
        if (out_data is None):
            break
        pset = out_data[0]
        all_points = out_data[1]
        all_labels = out_data[2]
        logging.info('Post-processing {}'.format(pset.filename))
        with tempfile.TemporaryDirectory() as tmpdir:
            ipath = os.path.join(tmpdir, (pset.filename + '_original.las'))
            pset.save(ipath)
            pset.x = all_points[(:, 0)]
            pset.y = all_points[(:, 1)]
            pset.z = all_points[(:, 2)]
            pset.i = all_points[(:, 3)]
            pset.r = all_points[(:, 4)]
            pset.c = np.array([LABEL_MAP[v] for v in all_labels], dtype='uint8')
            cpath = os.path.join(tmpdir, (pset.filename + '_candidates.las'))
            pset.save(cpath)
            if (FLAGS.output_type is OutputType.LABELS):
                opath = os.path.join(tmpdir, (pset.filename + '.las'))
            else:
                opath = os.path.join(FLAGS.output_path, (pset.filename + '.las'))
            pipeline = {'pipeline': [ipath, {'type': 'filters.neighborclassifier', 'k': ((FLAGS.n_angles * 4) + 1), 'candidate': cpath}, opath]}
            p = subprocess.run(['/opt/conda/envs/cpdal-run/bin/pdal', 'pipeline', '-s'], input=json.dumps(pipeline).encode())
            if p.returncode:
                raise ValueError((('Failed to run pipeline: \n"' + json.dumps(pipeline)) + '"'))
            if (not (FLAGS.output_type is OutputType.LAS)):
                pset2 = PointSet(opath)
                pset2.save_classifications_txt(os.path.join(FLAGS.output_path, (pset.filename + '_CLS.txt')))
            output_queue.task_done()
            logging.debug('Finished {}'.format(pset.filename))
    logging.debug('Post-processing thread finished')
