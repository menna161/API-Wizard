from collections import deque
import cv2
import os
import gin
import gym
import numpy as np
import time
import pybullet_envs
from tasks import atari_wrappers
from tasks.base_task import BaseTask
from tasks.cartpole_env import CartPoleSwingUpHarderEnv


def __init__(self, env_name, shuffle_on_reset=False, render=False, v=True):
    super(PyBulletTask, self).__init__(v=v)
    self.env_name = env_name
    self.shuffle_on_reset = shuffle_on_reset
    self.perm_ix = 0
    self.render = render
    self.env = gym.make(self.env_name)
    self.perm_ix = np.arange(self.env.observation_space.shape[0])
    if self.render:
        self.env.render('human')
