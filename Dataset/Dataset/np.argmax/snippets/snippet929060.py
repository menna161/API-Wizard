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


def step(self, action):
    index = np.argmax(action).astype(int)
    if self._strict:
        reference = np.zeros_like(action)
        reference[index] = 1
        assert np.allclose(reference, action), action
    return self._env.step(index)
