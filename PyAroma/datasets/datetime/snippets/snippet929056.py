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


def _get_obs(self):
    if (self._action_repeat > 1):
        np.maximum(self._buffers[0], self._buffers[1], out=self._buffers[0])
    image = skimage.transform.resize(self._buffers[0], output_shape=self._size, mode='edge', order=1, preserve_range=True)
    image = np.clip(image, 0, 255).astype(np.uint8)
    image = (image[(:, :, None)] if self._grayscale else image)
    return {'image': image}
