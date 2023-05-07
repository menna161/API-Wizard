import numpy as np
import random
import json
import sys
import config
from env import make_env
import time
import cma
from es import SimpleGA, CMAES, PEPG, OpenES
from gym.wrappers import Monitor
import tensorflow as tf


def __init__(self, game, peak=1.0):
    self.env_name = game.env_name
    self.layer_1 = game.layers[0]
    self.layer_2 = game.layers[1]
    self.world_hidden_size = self.layer_1
    self.agent_hidden_size = self.layer_2
    self.x_threshold = 2.4
    self.dt = 0.01
    self.peek_prob = peak
    self.peek_next = 1
    self.peek = 1
    self.rnn_mode = False
    self.experimental_mode = game.experimental_mode
    self.input_size = game.input_size
    self.output_size = game.output_size
    self.render_mode = False
    self.world_model = SimpleWorldModel(obs_size=self.input_size, action_size=self.output_size, hidden_size=self.world_hidden_size)
    self.agent = Agent(layer_1=self.agent_hidden_size, layer_2=32, input_size=self.input_size, output_size=6)
    self.param_count = (self.world_model.param_count + self.agent.param_count)
