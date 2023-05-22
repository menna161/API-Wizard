import numpy as np
import torch
import torch.nn.functional as F
import matplotlib
import threading
from matplotlib import collections as mc
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation
import time
import copy
import math
from neural_layout.barnes_hut_tree import *
from matplotlib import pyplot as plt


def simulation_step(self):
    f = torch.zeros_like(self.x)
    force_noise = (torch.randn_like(self.x) * self.noise)
    f += force_noise
    electrical_force = torch.zeros_like(f)
    if (self.repulsion != 0.0):
        if (self.mac > 0):
            mass = self.weights
            qt = BarnesHutTree(self.x, mass, device=self.device, max_levels=self.max_levels)
            electrical_force = qt.traverse(self.x, mass, mac=self.mac, force_function=self.repulsion_function)
        else:
            diff = (self.x.unsqueeze(0) - self.x.unsqueeze(1))
            m = (self.weights.unsqueeze(0) * self.weights.unsqueeze(1)).unsqueeze(2)
            electrical_force = torch.sum((m * (diff / ((torch.norm(diff, 2, dim=2, keepdim=True) ** 2) + 1e-05))), dim=0)
        electrical_force *= (self.repulsion * (self.spring_optimal_distance ** 2))
    f += electrical_force
    attraction_force = torch.zeros_like(f)
    if (self.spring_optimal_distance != 0.0):
        attraction_force = torch.zeros_like(f)
        diff = (self.x[self.network.connections[(:, 1)]] - self.x[self.network.connections[(:, 0)]])
        dist = torch.norm(diff, 2, dim=1, keepdim=True)
        a_f = ((diff * dist) / self.spring_optimal_distance)
        a_f *= self.connection_weights.unsqueeze(1)
        attraction_force.scatter_add_(0, self.network.connections[(:, 0:1)].repeat([1, self.num_dim]), a_f)
        attraction_force.scatter_add_(0, self.network.connections[(:, 1:2)].repeat([1, self.num_dim]), (- a_f))
        if (self.attraction_normalization > 0.0):
            attraction_force *= (self.avg_connection_count / (1 + (self.attraction_normalization * self.per_unit_connection_weight.unsqueeze(1))))
    f += attraction_force
    if (self.centering > 0.0):
        dist = torch.norm(self.x, 2, dim=1, keepdim=True)
        centering_force = ((((- self.centering) * (self.x / dist)) * (dist ** 2)) * self.weights.unsqueeze(1))
        f += centering_force
    f_norm = torch.norm(f, 2, dim=1)
    energy = torch.sum((f ** 2))
    out_of_bound = (f_norm > self.force_limit)
    f[out_of_bound] = ((self.force_limit * f[out_of_bound]) / f_norm[out_of_bound].unsqueeze(1))
    a = (f / self.weights.unsqueeze(1))
    self.v /= (1 + self.drag)
    self.v += ((0.5 * (self.a + a)) * self.step_size)
    self.a = a
    x_update = (self.movable.unsqueeze(1) * ((self.v * self.step_size) + ((0.5 * self.a) * (self.step_size ** 2))))
    is_nan = torch.isnan(x_update)
    if (torch.sum(is_nan) > 0):
        print('x updates with nan:', is_nan.nonzero())
        x_update[is_nan] = torch.zeros(torch.sum(is_nan), device=self.x.device)
    self.x += x_update
    self.update_step_size(energy)
    self.energy = energy
