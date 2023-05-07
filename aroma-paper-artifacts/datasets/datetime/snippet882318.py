import argparse
import json
import os
from datetime import datetime
from os import path
from pathlib import Path
import numpy as np
from mdp.plane_obstacles_mdp import PlanarObstaclesMDP
from PIL import Image
from tqdm import trange


def write_to_file(noise, sample_size):
    '\n    write [(x, u, x_next)] to output dir\n    '
    output_dir = (root_path + '/data/planar/raw_{:d}_{:.0f}'.format(sample_size, noise))
    if (not path.exists(output_dir)):
        os.makedirs(output_dir)
    (x_data, u_data, x_next_data, state_data, state_next_data) = sample(sample_size, noise)
    samples = []
    for (i, _) in enumerate(x_data):
        before_file = 'before-{:05d}.png'.format(i)
        Image.fromarray((x_data[i] * 255.0)).convert('L').save(path.join(output_dir, before_file))
        after_file = 'after-{:05d}.png'.format(i)
        Image.fromarray((x_next_data[i] * 255.0)).convert('L').save(path.join(output_dir, after_file))
        initial_state = state_data[i]
        after_state = state_next_data[i]
        u = u_data[i]
        samples.append({'before_state': initial_state.tolist(), 'after_state': after_state.tolist(), 'before': before_file, 'after': after_file, 'control': u.tolist()})
    with open(path.join(output_dir, 'data.json'), 'wt') as outfile:
        json.dump({'metadata': {'num_samples': sample_size, 'time_created': str(datetime.now()), 'version': 1}, 'samples': samples}, outfile, indent=2)
