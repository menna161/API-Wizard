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
    self.perm_ix = np.arange(self.env.observation_space.shape[0])
    if self.shuffle_on_reset:
        self.rnd.shuffle(self.perm_ix)
    if self.verbose:
        print('perm_ix: {}'.format(self.perm_ix))
    return super(CartPoleSwingUpTask, self).reset_for_rollout()
