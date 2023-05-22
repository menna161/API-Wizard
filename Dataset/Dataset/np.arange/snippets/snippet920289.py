import glfw
import OpenGL.GL as GL
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
import math
import glm
import ctypes
import time
import numpy as np
from PIL import Image


def add_voxel_map(self, voxel_map, voxel_map_center, voxel_size, filter_empty_voxels=True):
    '\n        Adds given voxel map to renderers voxel data\n        :param voxel_map: A 3D array in x-y-z format where each element is list of size 3 that represents color\n        :param voxel_map_center: Center of the voxel map\n        :param voxel_size: Size of voxels in meters\n        :param filter_empty_voxels: Filters out empty voxels if enabled\n        :return: None\n        '
    (x, y, z) = np.meshgrid(np.arange(0, voxel_map.shape[0]), np.arange(0, voxel_map.shape[1]), np.arange(0, voxel_map.shape[2]), indexing='ij')
    xyz_coordinates = np.array([x.flatten(), y.flatten(), z.flatten()], np.float32).T
    xyz_coordinates[(:, 0)] -= (voxel_map.shape[0] / 2)
    xyz_coordinates[(:, 1)] -= (voxel_map.shape[1] / 2)
    xyz_coordinates[(:, 2)] -= (voxel_map.shape[2] / 2)
    xyz_coordinates *= voxel_size
    xyz_coordinates += (voxel_size / 2)
    xyz_coordinates += voxel_map_center
    voxel_data = np.zeros(shape=(((voxel_map.shape[0] * voxel_map.shape[1]) * voxel_map.shape[2]), 7))
    flattened_map = voxel_map.reshape((- 1), 7)
    voxel_data[(:, :3)] = xyz_coordinates
    voxel_data[(:, 3)] = voxel_size
    voxel_data[(:, 4:)] = flattened_map[(:, :3)]
    if filter_empty_voxels:
        voxel_data = voxel_data[(voxel_data[(:, (- 1))] != 0)]
    self.add_voxels(voxel_data.flatten())
