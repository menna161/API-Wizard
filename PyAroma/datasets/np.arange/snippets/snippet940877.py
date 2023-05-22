from __future__ import print_function
import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from torch.autograd import Variable
import time


def __init__(self, equ_h, equ_w, RADIUS=128, CUDA=True, VAR=False):
    cen_x = ((equ_w - 1) / 2.0)
    cen_y = ((equ_h - 1) / 2.0)
    equ_h = int(equ_h)
    equ_w = int(equ_w)
    theta = (((2 * (np.arange(equ_w) - cen_x)) / equ_w) * np.pi)
    phi = (((2 * (np.arange(equ_h) - cen_y)) / equ_h) * (np.pi / 2))
    self.RADIUS = RADIUS
    theta = torch.FloatTensor(theta)
    phi = torch.FloatTensor(phi)
    if VAR:
        theta = Variable(theta)
        phi = Variable(phi)
    theta = theta.repeat(equ_h, 1)
    phi = phi.repeat(equ_w, 1).transpose(0, 1)
    x = ((RADIUS * torch.cos(phi)) * torch.sin(theta)).view(equ_h, equ_w, 1)
    y = (RADIUS * torch.sin(phi)).view(equ_h, equ_w, 1)
    z = ((RADIUS * torch.cos(phi)) * torch.cos(theta)).view(equ_h, equ_w, 1)
    self.xyz = torch.cat([x, y, z], dim=2).view(1, equ_h, equ_w, 3)
    self.CUDA = CUDA
