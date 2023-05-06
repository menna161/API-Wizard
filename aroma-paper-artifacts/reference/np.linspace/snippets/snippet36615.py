from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import tensorflow as tf
import argparse
import glob
import cv2
import numpy as np
import pickle
import random
import collections
from time import time
from tensorflow.python.client import device_lib


def LoadChunk(filename):
    global cached, dictionary
    fn = filename
    if (cached and (filename in dictionary)):
        return dictionary[filename]
    root = filename[:(- 16)]
    global view_pairs, intrinsic, kernel
    if (not isinstance(filename, str)):
        filename = filename.decode('utf-8')
    index = int(filename[(- 15):(- 10)])
    root = filename[:(- 16)]
    (color_src, uv_src, depth_src, mask_src, world2cam_src) = LoadDataByID(root, index)
    rindex = random.choice(view_pairs[index])
    if (rindex != index):
        (color_tar, uv_tar, depth_tar, mask_tar, world2cam_tar) = LoadDataByID(root, rindex)
        cam2world_src = np.linalg.inv(world2cam_src)
        src2tar = np.transpose(np.dot(world2cam_tar, cam2world_src))
        y = np.linspace(0, (IMAGE_HEIGHT - 1), IMAGE_HEIGHT)
        x = np.linspace(0, (IMAGE_WIDTH - 1), IMAGE_WIDTH)
        (xx, yy) = np.meshgrid(x, y)
        fx = intrinsic[0]
        cx = intrinsic[2]
        fy = intrinsic[5]
        cy = intrinsic[6]
        x = (((xx - cx) / fx) * depth_src)
        y = (((yy - cy) / fy) * depth_src)
        coords = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 4))
        coords[(:, :, 0)] = x
        coords[(:, :, 1)] = y
        coords[(:, :, 2)] = depth_src
        coords[(:, :, 3)] = 1
        coords = np.dot(coords, src2tar)
        z_tar = coords[(:, :, 2)]
        x = (((coords[(:, :, 0)] / (1e-08 + z_tar)) * fx) + cx)
        y = (((coords[(:, :, 1)] / (1e-08 + z_tar)) * fy) + cy)
        mask0 = (depth_src == 0)
        mask1 = ((((x < 0) + (y < 0)) + (x >= (IMAGE_WIDTH - 1))) + (y >= (IMAGE_HEIGHT - 1)))
        lx = np.floor(x).astype('float32')
        ly = np.floor(y).astype('float32')
        rx = (lx + 1).astype('float32')
        ry = (ly + 1).astype('float32')
        sample_z1 = np.abs((z_tar - cv2.remap(depth_tar, lx, ly, cv2.INTER_NEAREST)))
        sample_z2 = np.abs((z_tar - cv2.remap(depth_tar, lx, ry, cv2.INTER_NEAREST)))
        sample_z3 = np.abs((z_tar - cv2.remap(depth_tar, rx, ly, cv2.INTER_NEAREST)))
        sample_z4 = np.abs((z_tar - cv2.remap(depth_tar, rx, ry, cv2.INTER_NEAREST)))
        mask2 = (np.minimum(np.minimum(sample_z1, sample_z2), np.minimum(sample_z3, sample_z4)) > 0.1)
        mask_remap = (1 - (((mask0 + mask1) + mask2) > 0)).astype('float32')
        map_x = x.astype('float32')
        map_y = y.astype('float32')
        color_tar_to_src = cv2.remap(color_tar, map_x, map_y, cv2.INTER_LINEAR)
        mask = ((cv2.remap(mask_tar, map_x, map_y, cv2.INTER_LINEAR) > 0.99) * mask_remap)
        for j in range(3):
            color_tar_to_src[(:, :, j)] *= mask
    else:
        color_tar_to_src = color_src.copy()
        mask = mask_src.copy()
    color_src = ((color_src * 2.0) - 1.0).astype('float32')
    color_tar_to_src = ((color_tar_to_src * 2.0) - 1.0).astype('float32')
    uv_src[(:, :, 1)] = (1 - uv_src[(:, :, 1)])
    uv_src[(:, :, 0)] *= (tex_dim_width - 1)
    uv_src[(:, :, 1)] *= (tex_dim_height - 1)
    for i in range(3):
        color_src[(:, :, i)] *= mask
        color_tar_to_src[(:, :, i)] *= mask
    if cached:
        dictionary[fn] = (color_src, color_tar_to_src, uv_src, np.reshape(mask, (mask.shape[0], mask.shape[1], 1)))
        return dictionary[fn]
    return (color_src, color_tar_to_src, uv_src, np.reshape(mask, (mask.shape[0], mask.shape[1], 1)))
