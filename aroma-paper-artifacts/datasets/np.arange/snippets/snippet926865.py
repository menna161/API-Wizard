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


def reset_for_rollout(self):
    self.original_obs = None
    self.shuffled_obs = None
    self.obs_perm_ix = np.arange(((96 // self.patch_size) ** 2))
    if self.permute_obs:
        self.rnd.shuffle(self.obs_perm_ix)
    if (self.stack_k_frames > 0):
        self.obs_stack = deque(maxlen=self.stack_k_frames)
    self._neg_reward_cnt = 0
    return super(CarRacingTask, self).reset_for_rollout()
