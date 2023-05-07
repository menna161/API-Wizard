import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import torch
from colour import Color
from mdp.pendulum_mdp import PendulumMDP
from pc3_model import PC3
from torchvision.transforms import ToTensor


def assign_latent_color(model, angel, mdp):
    angle_vels = np.linspace(start=mdp.angular_velocity_range[0], stop=mdp.angular_velocity_range[1], num=num_each_angle)
    all_z_for_angle = []
    for i in range(num_each_angle):
        ang_velocity = angle_vels[i]
        s = np.array([angel, ang_velocity])
        x = mdp.render(s).squeeze()
        u = mdp.sample_random_action()
        s_next = mdp.transition_function(s, u)
        x_next = mdp.render(s_next).squeeze()
        x_with_history = np.vstack((x_next, x))
        x_with_history = ToTensor()(x_with_history).double()
        with torch.no_grad():
            z = model.encode(x_with_history.view((- 1), (x_with_history.shape[(- 1)] * x_with_history.shape[(- 2)])))
        all_z_for_angle.append(z.detach().squeeze().numpy())
    return all_z_for_angle
