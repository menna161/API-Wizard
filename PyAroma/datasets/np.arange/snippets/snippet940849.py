import numpy as np
from functools import partial
import vispy
from vispy import app, gloo, visuals, scene


def SphereGrid(equ_h, equ_w):
    cen_x = ((equ_w - 1) / 2.0)
    cen_y = ((equ_h - 1) / 2.0)
    theta = (((2 * (np.arange(equ_w) - cen_x)) / equ_w) * np.pi)
    phi = (((2 * (np.arange(equ_h) - cen_y)) / equ_h) * (np.pi / 2))
    theta = np.tile(theta[(None, :)], [equ_h, 1])
    phi = np.tile(phi[(None, :)], [equ_w, 1]).T
    x = (np.cos(phi) * np.sin(theta)).reshape([equ_h, equ_w, 1])
    y = np.sin(phi).reshape([equ_h, equ_w, 1])
    z = (np.cos(phi) * np.cos(theta)).reshape([equ_h, equ_w, 1])
    xyz = np.concatenate([x, y, z], axis=(- 1))
    return xyz
