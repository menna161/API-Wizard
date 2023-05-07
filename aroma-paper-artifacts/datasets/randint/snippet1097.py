import numpy as np
import os
from collections import deque
import gym
from gym import spaces
import cv2
from copy import deepcopy


def reset(self, **kwargs):
    ' Do no-op action for a number of steps in [1, noop_max].'
    self.env.reset(**kwargs)
    if (self.override_num_noops is not None):
        noops = self.override_num_noops
    else:
        noops = self.unwrapped.np_random.randint(1, (self.noop_max + 1))
    assert (noops > 0)
    obs = None
    for _ in range(noops):
        (obs, _, done, _) = self.env.step(self.noop_action)
        if done:
            obs = self.env.reset(**kwargs)
    return obs
