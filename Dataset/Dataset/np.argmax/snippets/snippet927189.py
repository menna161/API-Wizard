import numpy as np
import random
import json
import cma
from es import SimpleGA, CMAES, PEPG, OpenES
from env import make_env


def sample(p):
    return np.argmax(np.random.multinomial(1, p))
