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


def sample(p):
    return np.argmax(np.random.multinomial(1, p))