import sys
import datetime
import subprocess
from distutils import dir_util
import numpy as np
import os
from PIL import Image
import tensorflow as tf
from wavedata.tools.core import calib_utils
import avod
from avod.core import box_3d_projector
from avod.core import summary_utils


def set_up_summary_writer(model_config, sess):
    ' Helper function to set up log directories and summary\n        handlers.\n    Args:\n        model_config: Model protobuf configuration\n        sess : A tensorflow session\n    '
    paths_config = model_config.paths_config
    logdir = paths_config.logdir
    if (not os.path.exists(logdir)):
        os.makedirs(logdir)
    logdir = (logdir + '/eval')
    datetime_str = str(datetime.datetime.now())
    summary_writer = tf.summary.FileWriter(((logdir + '/') + datetime_str), sess.graph)
    global_summaries = set([])
    summaries = set(tf.get_collection(tf.GraphKeys.SUMMARIES))
    summary_merged = summary_utils.summaries_to_keep(summaries, global_summaries, histograms=False, input_imgs=False, input_bevs=False)
    return (summary_writer, summary_merged)
