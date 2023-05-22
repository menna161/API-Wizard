import tensorflow as tf
import numpy as np


def calculateSmoothness(DVF, voxelSize=[1, 1]):
    '\n    :param DVF: a numpy array with shape of (2, sizeY, sizeX) or (3, sizeZ, sizeY, sizeX). You might use np.transpose before this function to correct the order of DVF shape.\n    :param voxelSize: physical voxel spacing in mm\n    :return: Jac\n    Hessam Sokooti h.sokooti@gmail.com\n    '
    if ((len(np.shape(DVF)) - 1) != len(voxelSize)):
        raise ValueError('dimension of DVF is {} but dimension of voxelSize is {}'.format((len(np.shape(DVF)) - 1), len(voxelSize)))
    T = np.zeros(np.shape(DVF), dtype=np.float32)
    indices = ([None] * (len(np.shape(DVF)) - 1))
    DVF_grad = {}
    if (len(voxelSize) == 2):
        (indices[0], indices[1]) = np.meshgrid(np.arange(0, np.shape(DVF)[1]), np.arange(0, np.shape(DVF)[2]), indexing='ij')
    if (len(voxelSize) == 3):
        (indices[0], indices[1], indices[2]) = np.meshgrid(np.arange(0, np.shape(DVF)[1]), np.arange(0, np.shape(DVF)[2]), np.arange(0, np.shape(DVF)[3]), indexing='ij')
    for d in range(len(voxelSize)):
        indices[d] = (indices[d] * voxelSize[d])
        T[(d, :)] = (DVF[(d, :)] + indices[d])
    for d in range(len(voxelSize)):
        DVF_grad[('dim' + str(d))] = []
        DVF_grad[('dim' + str(d))] = np.diff(T, n=1, axis=(d + 1))
        for d2 in range(d, len(voxelSize)):
            DVF_grad[(('dim' + str(d)), ('dim' + str(d2)))] = []
            DVF_grad[(('dim' + str(d)), ('dim' + str(d2)))] = np.diff(DVF_grad[('dim' + str(d))], n=1, axis=(d2 + 1))
            padAfter = np.zeros((len(voxelSize) + 1), dtype=np.int8)
            padAfter[(d + 1)] = (padAfter[(d + 1)] + 1)
            padAfter[(d2 + 1)] = (padAfter[(d2 + 1)] + 1)
            if (len(voxelSize) == 2):
                DVF_grad[(('dim' + str(d)), ('dim' + str(d2)))] = np.pad(DVF_grad[(('dim' + str(d)), ('dim' + str(d2)))], ((0, 0), (0, padAfter[1]), (0, padAfter[2])), 'constant', constant_values=(0,))
            if (len(voxelSize) == 3):
                DVF_grad[(('dim' + str(d)), ('dim' + str(d2)))] = np.pad(DVF_grad[(('dim' + str(d)), ('dim' + str(d2)))], ((0, 0), (0, padAfter[1]), (0, padAfter[2]), (0, padAfter[3])), 'constant', constant_values=(0,))
    if (len(voxelSize) == 2):
        smoothness = np.mean(((np.square(DVF_grad[('dim0', 'dim0')]) + (2 * np.square(DVF_grad[('dim0', 'dim1')]))) + np.square(DVF_grad[('dim1', 'dim1')])))
    if (len(voxelSize) == 3):
        smoothness = np.mean((((((np.square(DVF_grad[('dim0', 'dim0')]) + (2 * np.square(DVF_grad[('dim0', 'dim1')]))) + (2 * np.square(DVF_grad[('dim0', 'dim2')]))) + np.square(DVF_grad[('dim1', 'dim1')])) + (2 * np.square(DVF_grad[('dim1', 'dim2')]))) + np.square(DVF_grad[('dim2', 'dim2')])))
    return smoothness
