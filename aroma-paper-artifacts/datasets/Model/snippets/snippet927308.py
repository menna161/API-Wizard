import numpy as np
import random
import json
import sys
import config
from env import make_env
import time
import os
import cma
from es import SimpleGA, CMAES, PEPG, OpenES
from gym.wrappers import Monitor
import imageio


def make_model(game):
    if game.experimental_mode:
        model = CustomModel(game)
    else:
        model = Model(game)
    return model
