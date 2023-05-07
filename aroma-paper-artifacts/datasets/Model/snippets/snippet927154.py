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
    self.env_name = game.env_name
    self.layer_1 = game.layers[0]
    self.layer_2 = game.layers[1]
    self.world_hidden_size = self.layer_1
    self.agent_hidden_size = self.layer_2
    self.rnn_mode = True
    self.experimental_mode = False
    self.input_size = game.input_size
    self.output_size = game.output_size
    self.render_mode = False
    self.dropout_keep_prob = 1.0
    self.world_model = RNNWorldModel(obs_size=self.input_size, action_size=self.output_size, hidden_size=self.world_hidden_size, dropout_keep_prob=self.dropout_keep_prob, predict_future=False)
    self.agent = Agent(layer_1=self.agent_hidden_size, layer_2=0, input_size=(self.input_size + (self.world_hidden_size * 2)), output_size=self.output_size)
    self.param_count = (self.world_model.param_count + self.agent.param_count)
