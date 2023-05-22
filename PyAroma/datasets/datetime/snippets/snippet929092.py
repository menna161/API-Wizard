from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import atexit
import datetime
import io
import os
import sys
import threading
import traceback
import uuid
import gym
import gym.spaces
import numpy as np
import skimage.transform
import tensorflow as tf
from dreamer import tools
import deepmind_lab
import gym
from dm_control import suite
import multiprocessing.dummy as mp
import multiprocessing as mp


def _get_filename(self, episode):
    timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    identifier = str(uuid.uuid4().hex)
    length = len(episode['reward'])
    filename = '{}-{}-{}.npz'.format(timestamp, identifier, length)
    filename = os.path.join(self._outdir, filename)
    return filename
