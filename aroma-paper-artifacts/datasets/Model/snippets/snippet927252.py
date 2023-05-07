import logging
import math
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
from model import SimpleWorldModel
from config import games
from gym.envs.classic_control import rendering


def __init__(self):
    self.t = 0
    self.t_limit = 1000
    self.x_threshold = 2.4
    self.dt = 0.01
    self.real_obs_size = 5
    self.hidden_size = games['learn_cartpole'].layers[0]
    self.world_model = SimpleWorldModel(obs_size=self.real_obs_size, hidden_size=self.hidden_size)
    self.param_count = self.world_model.param_count
    self.world_model.load_model('./log/learn_cartpole.pepg.16.384.best.json')
    high = np.array(([np.finfo(np.float32).max] * self.real_obs_size))
    self.action_space = spaces.Box((- 1.0), 1.0, shape=(1,))
    self.observation_space = spaces.Box((- high), high)
    self._seed()
    self.viewer = None
