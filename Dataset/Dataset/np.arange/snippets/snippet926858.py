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


def __init__(self, shuffle_on_reset=False, render=False, v=True, num_noise_channels=0):
    super(CartPoleSwingUpTask, self).__init__(v=v)
    self.shuffle_on_reset = shuffle_on_reset
    self.perm_ix = 0
    self.render = render
    self.env = CartPoleSwingUpHarderEnv()
    self.perm_ix = np.arange(self.env.observation_space.shape[0])
    self.noise_std = 0.1
    self.num_noise_channels = num_noise_channels
    self.rnd = np.random.RandomState(seed=0)
