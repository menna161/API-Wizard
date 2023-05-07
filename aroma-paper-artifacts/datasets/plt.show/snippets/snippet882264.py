import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import torch
from colour import Color
from mdp.pendulum_mdp import PendulumMDP
from pc3_model import PC3
from torchvision.transforms import ToTensor


def show_latent_map(model, mdp):
    (angle_color_map, colors_rgb) = map_angle_color(num_angles, mdp)
    colors_list = []
    for color in colors_rgb:
        for i in range(num_each_angle):
            colors_list.append(list(color))
    all_z = []
    for angle in angle_color_map:
        all_z_for_angle = assign_latent_color(model, angle, mdp)
        all_z += all_z_for_angle
    all_z = np.array(all_z)
    z_min = np.min(all_z, axis=0)
    z_max = np.max(all_z, axis=0)
    all_z = (((2 * (all_z - z_min)) / (z_max - z_min)) - 1.0)
    all_z = (all_z * 35)
    ax = plt.axes(projection='3d')
    ax.set_xlim([(- 60), 60])
    ax.set_ylim([(- 60), 60])
    ax.set_zlim([(- 60), 60])
    xdata = all_z[(:, 0)]
    ydata = all_z[(:, 1)]
    zdata = all_z[(:, 2)]
    ax.scatter(xdata, ydata, zdata, c=colors_list, marker='o', s=10)
    plt.show()
