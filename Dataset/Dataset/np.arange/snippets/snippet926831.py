from collections import deque
import gym
import numpy as np
from gym import spaces
import cv2


def reset(self, **kwargs):
    self.patch_to_keep_ix = None
    self.perm_ix = np.arange(self.num_patches)
    self.zero_out_ix = np.arange(self.num_patches)
    self.np_random.shuffle(self.zero_out_ix)
    if self.permute_obs:
        self.np_random.shuffle(self.perm_ix)
    self.step_cnt = 0
    return super(PermuteWarpFrame, self).reset(**kwargs)
