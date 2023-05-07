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


def make_model(game, peak=1.0):
    if game.experimental_mode:
        model = CustomModel(game, peak=peak)
    else:
        model = Model(game)
    return model
