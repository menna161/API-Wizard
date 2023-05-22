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


def reset(self):
    self._done = False
    self._env.reset(seed=self._random.randint(0, ((2 ** 31) - 1)))
    obs = self._get_obs()
    return obs
