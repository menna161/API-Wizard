from collections import deque
import gym
import numpy as np
from gym import spaces
import cv2


def __init__(self, env, channel_order='hwc', permute_obs=True, rand_zero_out_ratio=0.0, patch_size=6):
    'Warp frames to 84x84 as done in the Nature paper and later work.'
    gym.ObservationWrapper.__init__(self, env)
    self.width = 84
    self.height = 84
    shape = {'hwc': (self.height, self.width, 1), 'chw': (1, self.height, self.width)}
    self.observation_space = spaces.Box(low=0, high=255, shape=shape[channel_order], dtype=np.uint8)
    self.original_obs = None
    self.shuffled_obs = None
    self.gray_obs = None
    self.permute_obs = permute_obs
    self.rand_zero_out_ratio = rand_zero_out_ratio
    self.patch_size = patch_size
    self.num_patches = ((84 // self.patch_size) ** 2)
    self.perm_ix = np.arange(self.num_patches)
    self.zero_out_ix = np.arange(self.num_patches)
    self.np_random = np.random.RandomState(0)
    self.step_cnt = 0
    self.patch_to_keep_ix = None
