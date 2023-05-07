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


def make_model(game):
    if game.rnn_mode:
        model = RNNModel(game)
    elif game.experimental_mode:
        model = CustomModel(game)
    else:
        model = Model(game)
    return model
