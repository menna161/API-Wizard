from collections import deque
import gym
import numpy as np
from gym import spaces
import cv2


def reset(self, **kwargs):
    'Do no-op action for a number of steps in [1, noop_max].'
    self.env.reset(**kwargs)
    if (self.override_num_noops is not None):
        noops = self.override_num_noops
    else:
        noops = self.unwrapped.np_random.randint(1, (self.noop_max + 1))
    assert (noops > 0)
    obs = None
    for _ in range(noops):
        (obs, _, done, info) = self.env.step(self.noop_action)
        if (done or info.get('needs_reset', False)):
            obs = self.env.reset(**kwargs)
    return obs
