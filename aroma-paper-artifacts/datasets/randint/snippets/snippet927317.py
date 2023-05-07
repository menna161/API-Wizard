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


def main():
    global RENDER_DELAY
    assert (len(sys.argv) > 1), 'python model.py gamename path_to_mode.json'
    gamename = sys.argv[1]
    if gamename.startswith('bullet'):
        RENDER_DELAY = True
    use_model = False
    game = config.games[gamename]
    if (len(sys.argv) > 2):
        use_model = True
        filename = sys.argv[2]
        print('filename', filename)
    the_seed = np.random.randint(100000000)
    if (len(sys.argv) > 3):
        the_seed = int(sys.argv[3])
        print('seed', the_seed)
    model = make_model(game)
    print('model size', model.param_count)
    model.make_env(render_mode=render_mode)
    if use_model:
        model.load_model(filename)
    else:
        params = model.get_random_model_params(stdev=1.0)
        model.set_model_params(params)
    if final_mode:
        rewards = []
        for i in range(100):
            (reward, steps_taken) = simulate(model, train_mode=False, render_mode=False, num_episode=1, seed=(the_seed + i))
            rewards.append(reward[0])
        print('seed', the_seed, ', average_reward', np.mean(rewards), ', standard_deviation', np.std(rewards))
    else:
        if record_video:
            model.env = Monitor(model.env, directory=('/tmp/' + gamename), video_callable=(lambda episode_id: True), write_upon_reset=True, force=True)
        for i in range(1):
            (reward, steps_taken) = simulate(model, train_mode=False, render_mode=render_mode, num_episode=1, seed=(the_seed + i))
            print('terminal reward', reward, 'average steps taken', (np.mean(steps_taken) + 1))
