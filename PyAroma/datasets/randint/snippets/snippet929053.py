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
    with self.LOCK:
        self._env.reset()
    noops = (self._random.randint(1, self._noops) if (self._noops > 1) else 1)
    for _ in range(noops):
        done = self._env.step(0)[2]
        if done:
            with self.LOCK:
                self._env.reset()
    self._lives = self._env.ale.lives()
    if self._grayscale:
        self._env.ale.getScreenGrayscale(self._buffers[0])
    else:
        self._env.ale.getScreenRGB2(self._buffers[0])
    self._buffers[1].fill(0)
    return self._get_obs()
