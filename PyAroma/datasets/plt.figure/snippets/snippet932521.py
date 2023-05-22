from baseline_racer import BaselineRacer
from gtp_visualize import *
from utils import to_airsim_vector, to_airsim_vectors
import airsimneurips as airsim
import argparse
import gtp
import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def __init__(self, traj_params, drone_names, drone_i, drone_params, use_vel_constraints=False, plot_gtp=False):
    super().__init__(drone_name=drone_names[drone_i], viz_traj=True)
    self.drone_names = drone_names
    self.drone_i = drone_i
    self.drone_params = drone_params
    self.traj_params = traj_params
    self.use_vel_constraints = use_vel_constraints
    self.plot_gtp = plot_gtp
    self.controller = None
    if self.plot_gtp:
        (self.fig, self.ax) = plt.subplots()
        self.line_state = None
        self.lines = ([None] * 2)
        self.fig2 = plt.figure(2)
        self.ax3d = self.fig2.add_subplot(111, projection='3d')
    print('baseline_racer_gtp ready!')
    if self.traj_params.blocking:
        print('   with blocking behavior activated')
