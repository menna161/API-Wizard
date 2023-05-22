import os
import sys
import cv2
import time
import numpy as np
import torch
import torch.nn.functional as F
from torch.autograd import Variable


def __init__(self, batch_size, equ_h, equ_w, out_dim, FOV, RADIUS=128, CUDA=True):
    batch_size = 1
    R_lst = []
    theta_lst = ((np.array([(- 90), 0, 90, 180], np.float) / 180) * np.pi)
    phi_lst = ((np.array([90, (- 90)], np.float) / 180) * np.pi)
    self.equ_h = equ_h
    self.equ_w = equ_w
    self.CUDA = CUDA
    for theta in theta_lst:
        angle_axis = (theta * np.array([0, 1, 0], np.float))
        R = cv2.Rodrigues(angle_axis)[0]
        R_lst.append(R)
    for phi in phi_lst:
        angle_axis = (phi * np.array([1, 0, 0], np.float))
        R = cv2.Rodrigues(angle_axis)[0]
        R_lst.append(R)
    R_lst = [Variable(torch.FloatTensor(x)) for x in R_lst]
    self.out_dim = out_dim
    equ_cx = ((equ_w - 1) / 2.0)
    equ_cy = ((equ_h - 1) / 2.0)
    c_x = ((out_dim - 1) / 2.0)
    c_y = ((out_dim - 1) / 2.0)
    wangle = ((180 - FOV) / 2.0)
    w_len = (((2 * RADIUS) * np.sin(np.radians((FOV / 2.0)))) / np.sin(np.radians(wangle)))
    f = ((RADIUS / w_len) * out_dim)
    cx = c_x
    cy = c_y
    self.intrisic = {'f': float(f), 'cx': float(cx), 'cy': float(cy)}
    interval = (w_len / (out_dim - 1))
    z_map = (np.zeros([out_dim, out_dim], np.float32) + RADIUS)
    x_map = np.tile(((np.arange(out_dim) - c_x) * interval), [out_dim, 1])
    y_map = np.tile(((np.arange(out_dim) - c_y) * interval), [out_dim, 1]).T
    D = np.sqrt((((x_map ** 2) + (y_map ** 2)) + (z_map ** 2)))
    xyz = np.zeros([out_dim, out_dim, 3], np.float)
    xyz[(:, :, 0)] = ((RADIUS / D) * x_map[(:, :)])
    xyz[(:, :, 1)] = ((RADIUS / D) * y_map[(:, :)])
    xyz[(:, :, 2)] = ((RADIUS / D) * z_map[(:, :)])
    if CUDA:
        xyz = Variable(torch.FloatTensor(xyz))
    else:
        xyz = Variable(torch.FloatTensor(xyz))
    reshape_xyz = xyz.view((out_dim * out_dim), 3).transpose(0, 1)
    self.batch_size = batch_size
    self.loc = []
    self.grid = []
    for (i, R) in enumerate(R_lst):
        result = torch.matmul(R, reshape_xyz).transpose(0, 1)
        tmp_xyz = result.contiguous().view(1, out_dim, out_dim, 3)
        self.grid.append(tmp_xyz)
        lon = (torch.atan2(result[(:, 0)], result[(:, 2)]).view(1, out_dim, out_dim, 1) / np.pi)
        lat = (torch.asin((result[(:, 1)] / RADIUS)).view(1, out_dim, out_dim, 1) / (np.pi / 2))
        self.loc.append(torch.cat([lon.repeat(batch_size, 1, 1, 1), lat.repeat(batch_size, 1, 1, 1)], dim=3))
    new_lst = [3, 5, 1, 0, 2, 4]
    self.R_lst = [R_lst[x] for x in new_lst]
    self.grid_lst = []
    for iii in new_lst:
        grid = self.grid[iii].clone()
        scale = (self.intrisic['f'] / grid[(:, :, :, 2:3)])
        grid *= scale
        self.grid_lst.append(grid)
