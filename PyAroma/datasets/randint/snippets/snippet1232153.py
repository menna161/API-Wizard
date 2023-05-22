import numpy as np
import gym, gym.spaces
import time
import os
from collections import OrderedDict
import yaml


def reset_env(self):
    self.agent_pos = self.traversable_tiles_left[np.random.randint(0, len(self.traversable_tiles_left))]
    self.agent_orientation = np.random.randint(4)
    self.target_pos = self.traversable_tiles_right[np.random.randint(0, len(self.traversable_tiles_right))].copy()
    self.target_pos[1] += (self.door_col + 1)
    self.door_state = self.door_min_state
    self.n_step = 0
    self.normalized_potential = 1.0
    self.initial_potential = self.get_potential()
