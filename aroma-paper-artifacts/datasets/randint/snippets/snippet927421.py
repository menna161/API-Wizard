from model_grid import make_model as make_model_near
from model_grid_conv import make_model as make_model_conv
from model_grid_fc import make_model as make_model_fc
from model_grid import simulate_with_acts as simulate
import numpy as np
from collections import namedtuple
import os
import os
import copy
import concurrent.futures


def process_file(f):
    diff = {}
    p = f.split('p.')[1].split('.apple')[0]
    p = float(p)
    if (p not in diff):
        diff[p] = []
    model = make_model(game)
    model.load_model(f)
    model.make_env(render_mode=True)
    model.env.reset()
    dir_data = {0: [], 1: [], 2: [], 3: [], 4: []}
    rew_data = worker(model, np.random.randint(1000000000))
    diff[p].append(rew_data[0])
    return diff
