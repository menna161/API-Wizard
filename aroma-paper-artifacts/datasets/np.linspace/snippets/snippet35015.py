import gym
import time
import numpy as np
from senseact import utils
from senseact.rtrl_base_env import RTRLBaseEnv
from senseact.devices.dxl import dxl_mx64
from senseact.devices.dxl.dxl_setup import setups
from senseact.devices.dxl import dxl_communicator as gcomm
from math import pi
from collections import deque
from multiprocessing import Array, Value
from rllab.spaces import Box as RlBox
from gym.spaces import Box as GymBox
from rllab.envs.env_spec import EnvSpec


def generate_trajectory(self):
    'Generate a variable speed target trajectory for the episode.'
    direction = self._rand_obj_.choice([(- 1), 1])
    if (direction == 1):
        start_pos = self._rand_obj_.uniform(low=self.angle_low, high=self.reset_pos_center)
        self.trajectory = np.linspace(start_pos, self.angle_high, self.comm_episode_length_step)
    else:
        start_pos = self._rand_obj_.uniform(low=self.reset_pos_center, high=self.angle_high)
        self.trajectory = np.linspace(start_pos, self.angle_low, self.comm_episode_length_step)
