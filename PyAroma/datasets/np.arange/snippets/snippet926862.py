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


def __init__(self, bkg=None, permute_obs=False, patch_size=6, out_of_track_cap=20, stack_k_frames=0, render=False):
    super(CarRacingTask, self).__init__()
    self.permute_obs = permute_obs
    self.patch_size = patch_size
    self.bkg = bkg
    bkg_file = os.path.join(os.path.dirname(__file__), 'bkg/{}.jpg'.format(self.bkg))
    if os.path.exists(bkg_file):
        self.bkg = cv2.resize(cv2.imread(bkg_file), (96, 96))[(:, :, ::(- 1))]
    else:
        self.bkg = None
    self.original_obs = None
    self.shuffled_obs = None
    self.obs_perm_ix = np.arange(((96 // self.patch_size) ** 2))
    self.rnd = np.random.RandomState(seed=0)
    self.solution = None
    self.render = render
    self._max_steps = 1000
    self._neg_reward_cnt = 0
    self._neg_reward_cap = out_of_track_cap
    self._action_high = np.array([1.0, 1.0, 1.0])
    self._action_low = np.array([(- 1.0), 0.0, 0.0])
    self.env = gym.make('CarRacing-v0')
    self.stack_k_frames = stack_k_frames
    if (self.stack_k_frames > 0):
        self.obs_stack = deque(maxlen=self.stack_k_frames)
