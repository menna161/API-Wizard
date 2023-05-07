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


def sample(env_name, sample_size, noise):
    '\n    return [(x, u, x_next, s, s_next)]\n    '
    (width, height, frequency) = (widths[env_name], heights[env_name], frequencies[env_name])
    s_dim = state_dims[env_name]
    mdp = mdps[env_name](width=width, height=height, frequency=frequency, noise=noise)
    x_data = np.zeros((sample_size, width, height, 2), dtype='float32')
    u_data = np.zeros((sample_size, mdp.action_dim), dtype='float32')
    x_next_data = np.zeros((sample_size, width, height, 2), dtype='float32')
    state_data = np.zeros((sample_size, s_dim, 2), dtype='float32')
    state_next_data = np.zeros((sample_size, s_dim, 2), dtype='float32')
    for sample in trange(sample_size, desc=(('Sampling ' + env_name) + ' data')):
        s0 = mdp.sample_random_state()
        x0 = mdp.render(s0)
        a0 = mdp.sample_random_action()
        s1 = mdp.transition_function(s0, a0)
        x1 = mdp.render(s1)
        a1 = mdp.sample_random_action()
        s2 = mdp.transition_function(s1, a1)
        x2 = mdp.render(s2)
        x_data[(sample, :, :, 0)] = x0[(:, :, 0)]
        x_data[(sample, :, :, 1)] = x1[(:, :, 0)]
        state_data[(sample, :, 0)] = s0
        state_data[(sample, :, 1)] = s1
        u_data[sample] = a1
        x_next_data[(sample, :, :, 0)] = x1[(:, :, 0)]
        x_next_data[(sample, :, :, 1)] = x2[(:, :, 0)]
        state_next_data[(sample, :, 0)] = s1
        state_next_data[(sample, :, 1)] = s2
    return (x_data, u_data, x_next_data, state_data, state_next_data)
