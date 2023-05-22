import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import torch
from colour import Color
from mdp.pendulum_mdp import PendulumMDP
from pc3_model import PC3
from torchvision.transforms import ToTensor


def map_angle_color(num_angles, mdp):
    colors = list(red.range_to(blue, num_angles))
    colors_rgb = [color.rgb for color in colors]
    all_angles = np.linspace(start=mdp.angle_range[0], stop=mdp.angle_range[1], num=num_angles)
    angle_color_map = dict(zip(all_angles, colors_rgb))
    return (angle_color_map, colors_rgb)
