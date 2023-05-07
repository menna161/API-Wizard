from __future__ import absolute_import, division, print_function
import argparse
import json
import os
import os.path as path
from datetime import datetime
from pathlib import Path
import numpy as np
from mdp.cartpole_mdp import CartPoleMDP
from mdp.pendulum_mdp import PendulumMDP
from mdp.three_pole_mdp import ThreePoleMDP
from PIL import Image
from tqdm import trange


def write_to_file(env_name, sample_size, noise):
    '\n    write [(x, u, x_next)] to output dir\n    '
    output_dir = (((root_path + '/data/') + env_name) + '/raw_{:d}_{:.0f}'.format(sample_size, noise))
    if (not path.exists(output_dir)):
        os.makedirs(output_dir)
    samples = []
    data = sample(env_name=env_name, sample_size=sample_size, noise=noise)
    (x_data, u_data, x_next_data, state_data, state_next_data) = data
    for i in range(x_data.shape[0]):
        x_1 = x_data[(i, :, :, 0)]
        x_2 = x_data[(i, :, :, 1)]
        before = np.hstack((x_1, x_2))
        before_file = 'before-{:05d}.png'.format(i)
        Image.fromarray((before * 255.0)).convert('L').save(path.join(output_dir, before_file))
        after_file = 'after-{:05d}.png'.format(i)
        x_next_1 = x_next_data[(i, :, :, 0)]
        x_next_2 = x_next_data[(i, :, :, 1)]
        after = np.hstack((x_next_1, x_next_2))
        Image.fromarray((after * 255.0)).convert('L').save(path.join(output_dir, after_file))
        initial_state = state_data[i]
        after_state = state_next_data[i]
        samples.append({'before_state': initial_state.tolist(), 'after_state': after_state.tolist(), 'before': before_file, 'after': after_file, 'control': u_data[i].tolist()})
    with open(path.join(output_dir, 'data.json'), 'wt') as outfile:
        json.dump({'metadata': {'num_samples': x_data.shape[0], 'time_created': str(datetime.now()), 'version': 1}, 'samples': samples}, outfile, indent=2)
