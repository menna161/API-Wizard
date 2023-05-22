import numpy as np
import random
import json
import sys
import config
from env import make_env
import time
import os
from gym.wrappers import Monitor
from nn import sigmoid, relu, passthru, softmax, sample, RNNModel
import imageio


def __init__(self, game):
    self.output_noise = game.output_noise
    self.env_name = game.env_name
    self.world_hidden_size = game.layers[0]
    self.agent_hidden_size = game.layers[1]
    self.rnn_mode = False
    self.experimental_mode = True
    self.peek_prob = PEEK_PROB
    self.simple_mode = SIMPLE_MODE
    self.peek_next = 1
    self.peek = 1
    self.counter = 0
    self.input_size = game.input_size
    self.output_size = game.output_size
    self.render_mode = False
    self.world_model = SimpleWorldModel(obs_size=self.input_size, action_size=self.output_size, hidden_size=self.world_hidden_size)
    agent_input_size = (self.input_size + self.world_hidden_size)
    if self.simple_mode:
        agent_input_size = self.input_size
    self.agent = Agent(layer_1=self.agent_hidden_size, layer_2=0, input_size=agent_input_size, output_size=self.output_size)
    self.param_count = (self.world_model.param_count + self.agent.param_count)
    self.prev_action = np.zeros(self.output_size)
    self.prev_prediction = None
