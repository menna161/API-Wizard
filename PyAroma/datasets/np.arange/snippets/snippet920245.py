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


@staticmethod
def convert_depthmap_to_points(depth_map, focal_length_in_pixels=None, principal_point=None, rgb_image=None, is_depth_along_z=True):
    '\n        Converts given depth map to point cloud\n        :param depth_map: A grayscale image where values are equal to depth in meters\n        :param focal_length_in_pixels: Focal lenght of the camera measured in pixels\n        :param principal_point: Center of image\n        :param rgb_image: Colored image that matches depth map, used for coloring points\n        :param is_depth_along_z: If True, z coordinate of the pixel will be equal to depth, otherwise depth will be\n        calculated as distance between camera and pixel\n        :return: List of points where each point is of form [x, y, z, r, g, b]\n        '
    if (focal_length_in_pixels is None):
        focal_length_in_pixels = 715
    if (principal_point is None):
        principal_point = [(depth_map.shape[0] / 2), (depth_map.shape[1] / 2)]
    if (depth_map.shape[0] == 1):
        depth_map = np.swapaxes(depth_map, 0, 1).swapaxes(1, 2)
    points = np.ones(shape=((depth_map.shape[0] * depth_map.shape[1]), 6))
    if (rgb_image is None):
        points[(:, 3:6)] = [0.5, 0.7, 1]
    else:
        if (rgb_image.shape[0] == 3):
            rgb_image = np.swapaxes(rgb_image, 0, 1).swapaxes(1, 2)
        rgb_image = rgb_image.reshape((- 1), 3)
        points[(:, 3:6)] = (rgb_image / 256.0)
    (y, x) = np.meshgrid(np.arange(0, depth_map.shape[1]), np.arange(0, depth_map.shape[0]))
    yx_coordinates = np.array([x.flatten(), y.flatten()], np.float32).T
    yx_coordinates += ((- 1) * np.array(principal_point))
    yx_coordinates = np.flip(yx_coordinates, 1)
    points[(:, 0:2)] = yx_coordinates
    points[(:, 2)] = depth_map.flatten()
    pixel_dist = (((points[(:, 0)] ** 2) + (points[(:, 1)] ** 2)) ** 0.5)
    focal_target_dist = (((focal_length_in_pixels ** 2) + (pixel_dist ** 2)) ** 0.5)
    if (not is_depth_along_z):
        points[(:, 2)] = ((points[(:, 2)] * focal_length_in_pixels) / focal_target_dist)
    points[(:, 0)] = ((points[(:, 0)] * points[(:, 2)]) / focal_length_in_pixels)
    points[(:, 1)] = ((points[(:, 1)] * points[(:, 2)]) / focal_length_in_pixels)
    points[(:, 1)] *= (- 1)
    return points
