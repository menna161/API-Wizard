import numpy as np
import os
from datetime import datetime
from collections import defaultdict
import torch
import yaml


def rotate_torch_vector(vector, roll, pitch, yaw):
    num_envs = vector.shape[0]
    device = vector.device
    rot_x = torch.zeros((num_envs, 3, 3), device=device)
    rot_x[(:, 0, 0)] = 1.0
    rot_x[(:, 0, 1)] = 0.0
    rot_x[(:, 0, 2)] = 0.0
    rot_x[(:, 1, 0)] = 0.0
    rot_x[(:, 1, 1)] = torch.cos((- roll))
    rot_x[(:, 1, 2)] = (- torch.sin((- roll)))
    rot_x[(:, 2, 0)] = 0.0
    rot_x[(:, 2, 1)] = torch.sin((- roll))
    rot_x[(:, 2, 2)] = torch.cos((- roll))
    rot_y = torch.zeros((num_envs, 3, 3), device=device)
    rot_y[(:, 0, 0)] = torch.cos((- pitch))
    rot_y[(:, 0, 1)] = 0.0
    rot_y[(:, 0, 2)] = torch.sin((- pitch))
    rot_y[(:, 1, 0)] = 0.0
    rot_y[(:, 1, 1)] = 1.0
    rot_y[(:, 1, 2)] = 0.0
    rot_y[(:, 2, 0)] = (- torch.sin((- pitch)))
    rot_y[(:, 2, 1)] = 0.0
    rot_y[(:, 2, 2)] = torch.cos((- pitch))
    rot_z = torch.zeros((num_envs, 3, 3), device=device)
    rot_z[(:, 0, 0)] = torch.cos((- yaw))
    rot_z[(:, 0, 1)] = (- torch.sin((- yaw)))
    rot_z[(:, 0, 2)] = 0.0
    rot_z[(:, 1, 0)] = torch.sin((- yaw))
    rot_z[(:, 1, 1)] = torch.cos((- yaw))
    rot_z[(:, 1, 2)] = 0.0
    rot_z[(:, 2, 0)] = 0.0
    rot_z[(:, 2, 1)] = 0.0
    rot_z[(:, 2, 2)] = 1.0
    vector = vector.unsqueeze(2)
    vector = torch.bmm(rot_x, vector)
    vector = torch.bmm(rot_y, vector)
    vector = torch.bmm(rot_z, vector)
    vector = vector.squeeze(2)
    return vector
