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
    action_data = np.asarray(rew_data[(- 1)])
    (unique, counts) = np.unique(action_data, return_counts=True)
    dir_dict = dict(zip(unique, ((1.0 * counts) / sum(counts))))
    for k in range(100):
        for direction in [0, 1, 2, 3, 4]:
            model.make_env(render_mode=True)
            model.env.reset()
            obs = model.env.observe()
            new_obs = model.env.step(direction)
            new_obs = new_obs[0]
            if (run_type == 'conv'):
                sample = model.world_model.window_deterministic_predict_next_state(obs, direction)
            if (run_type == 'near'):
                sample = model.world_model.near_sight_deterministic_predict_next_state(obs, direction)
            if (run_type == 'fc'):
                sample = model.world_model.deterministic_predict_next_state(obs, direction)
            diff_val = ((new_obs.reshape((- 1)) - sample.reshape((- 1))) ** 2.0).mean(axis=0)
            dir_data[direction].append(diff_val)
    mins = []
    mins_probs = []
    for i in [0, 1, 2, 3, 4]:
        mins.append(np.mean(dir_data[i]))
        if (i in dir_dict):
            mins_probs.append((np.mean(dir_data[i]), dir_dict[i]))
        else:
            mins_probs.append((np.mean(dir_data[i]), 0.0))
    cur_min = min(mins)
    index_of_min = 0
    for (i, k) in enumerate(mins):
        if (k == cur_min):
            index_of_min = i
    index_of_max = 0
    cur_max = 0
    for i in range(5):
        if (i in dir_dict):
            if (cur_max < dir_dict[i]):
                cur_max = dir_dict[i]
                index_of_max = i
    weighted_mins = 0
    for i in range(5):
        if (i in dir_dict):
            weighted_mins += (dir_dict[i] * mins[i])
    diff[p].append((cur_min, copy.deepcopy(rew_data[0]), mins_probs[index_of_max], weighted_mins))
    return diff
