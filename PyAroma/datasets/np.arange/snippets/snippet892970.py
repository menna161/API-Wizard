import math
import numpy as np
import os
import SimpleITK as sitk
import time
import functions.kernel.conv_kernel as conv_kernel
import functions.tf_utils as tfu
import tensorflow as tf
import tensorflow as tf
import tensorflow as tf
import matplotlib.pyplot as plt


def calculate_jac(dvf, voxel_size=None):
    '\n    :param dvf: a numpy array with shape of (sizeY, sizeX, 2) or (sizeZ, sizeY, sizeX, 3). You might use np.transpose before this function to correct the order of DVF shape.\n    :param voxel_size: physical voxel spacing in mm\n    :return: Jac\n    '
    if (voxel_size is None):
        voxel_size = [1, 1, 1]
    if ((len(np.shape(dvf)) - 1) != len(voxel_size)):
        raise ValueError('dimension of DVF is {} but dimension of voxelSize is {}'.format((len(np.shape(dvf)) - 1), len(voxel_size)))
    T = np.zeros(np.shape(dvf), dtype=np.float32)
    indices = ([None] * (len(np.shape(dvf)) - 1))
    dvf_grad = []
    if (len(voxel_size) == 2):
        (indices[0], indices[1]) = np.meshgrid(np.arange(0, np.shape(dvf)[0]), np.arange(0, np.shape(dvf)[1]), indexing='ij')
    if (len(voxel_size) == 3):
        (indices[0], indices[1], indices[2]) = np.meshgrid(np.arange(0, np.shape(dvf)[0]), np.arange(0, np.shape(dvf)[1]), np.arange(0, np.shape(dvf)[2]), indexing='ij')
    for d in range(len(voxel_size)):
        indices[d] = (indices[d] * voxel_size[d])
        T[(:, :, :, d)] = (dvf[(:, :, :, d)] + indices[d])
        dvf_grad.append([(grad_mat / voxel_size[d]) for grad_mat in np.gradient(T[(:, :, :, d)])])
    if (len(voxel_size) == 2):
        jac = ((dvf_grad[0][0] * dvf_grad[1][1]) - (dvf_grad[0][1] * dvf_grad[1][0]))
    elif (len(voxel_size) == 3):
        jac = (((((((dvf_grad[0][0] * dvf_grad[1][1]) * dvf_grad[2][2]) + ((dvf_grad[0][1] * dvf_grad[1][2]) * dvf_grad[2][0])) + ((dvf_grad[0][2] * dvf_grad[1][0]) * dvf_grad[2][1])) - ((dvf_grad[0][2] * dvf_grad[1][1]) * dvf_grad[2][0])) - ((dvf_grad[0][1] * dvf_grad[1][0]) * dvf_grad[2][2])) - ((dvf_grad[0][0] * dvf_grad[1][2]) * dvf_grad[2][1]))
    else:
        raise ValueError('Length of voxel size should be 2 or 3')
    return jac
