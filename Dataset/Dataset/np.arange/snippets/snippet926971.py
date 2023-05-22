import numpy as np
import random
import json
import sys
import config
from env import make_env
import time
import os
import ann
import argparse
from gym.wrappers import Monitor
import imageio


def main():
    global RENDER_DELAY
    parser = argparse.ArgumentParser(description='Train policy on OpenAI Gym environment using pepg, ses, openes, ga, cma')
    parser.add_argument('gamename', type=str, help='robo_pendulum, robo_ant, robo_humanoid, etc.')
    parser.add_argument('-f', '--filename', type=str, help='json filename', default='none')
    parser.add_argument('-e', '--eval_steps', type=int, default=100, help='evaluate this number of step if final_mode')
    parser.add_argument('-s', '--seed_start', type=int, default=0, help='initial seed')
    parser.add_argument('-w', '--single_weight', type=float, default=(- 100), help='single weight parameter')
    parser.add_argument('--stdev', type=float, default=2.0, help='standard deviation for weights')
    parser.add_argument('--sweep', type=int, default=(- 1), help='sweep a set of weights from -2.0 to 2.0 sweep times.')
    parser.add_argument('--lo', type=float, default=(- 2.0), help='slow side of sweep.')
    parser.add_argument('--hi', type=float, default=2.0, help='high side of sweep.')
    args = parser.parse_args()
    assert (len(sys.argv) > 1), 'python model.py gamename path_to_mode.json'
    gamename = args.gamename
    use_model = False
    game = config.games[gamename]
    filename = args.filename
    if (filename != 'none'):
        use_model = True
        print('filename', filename)
    the_seed = args.seed_start
    model = make_model(game)
    print('model size', model.param_count)
    eval_steps = args.eval_steps
    single_weight = args.single_weight
    weight_stdev = args.stdev
    num_sweep = args.sweep
    sweep_lo = args.lo
    sweep_hi = args.hi
    model.make_env(render_mode=render_mode)
    if use_model:
        model.load_model(filename)
    else:
        if (single_weight > (- 100)):
            params = model.get_single_model_params(weight=(single_weight - game.weight_bias))
            print('single weight value set to', single_weight)
        else:
            params = (model.get_uniform_random_model_params(stdev=weight_stdev) - game.weight_bias)
        model.set_model_params(params)
    if final_mode:
        if (num_sweep > 1):
            the_weights = np.arange(sweep_lo, (sweep_hi + ((sweep_hi - sweep_lo) / num_sweep)), ((sweep_hi - sweep_lo) / num_sweep))
            for i in range(len(the_weights)):
                the_weight = the_weights[i]
                params = model.get_single_model_params(weight=(the_weight - game.weight_bias))
                model.set_model_params(params)
                rewards = []
                for i in range(eval_steps):
                    (reward, steps_taken) = simulate(model, train_mode=False, render_mode=False, num_episode=1, seed=(the_seed + i))
                    rewards.append(reward[0])
                print('weight', the_weight, 'average_reward', np.mean(rewards), 'standard_deviation', np.std(rewards))
        else:
            rewards = []
            for i in range(eval_steps):
                ' random uniform params\n        params = model.get_uniform_random_model_params(stdev=weight_stdev)-game.weight_bias\n        model.set_model_params(params)\n        '
                (reward, steps_taken) = simulate(model, train_mode=False, render_mode=False, num_episode=1, seed=(the_seed + i))
                print(i, reward)
                rewards.append(reward[0])
            print('seed', the_seed, 'average_reward', np.mean(rewards), 'standard_deviation', np.std(rewards))
    else:
        if record_video:
            model.env = Monitor(model.env, directory=('/tmp/' + gamename), video_callable=(lambda episode_id: True), write_upon_reset=True, force=True)
        for i in range(1):
            (reward, steps_taken) = simulate(model, train_mode=False, render_mode=render_mode, num_episode=1, seed=(the_seed + i))
            print('terminal reward', reward, 'average steps taken', (np.mean(steps_taken) + 1))
