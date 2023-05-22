from __future__ import division
from __future__ import print_function
import os
import time
import scipy.io as io
import numpy as np
import random
import scipy.ndimage as nd
import matplotlib.pyplot as plt


def reshape_data(data_dir, filename, rand_voxels=None):
    voxels = getVoxelsFromMat(os.path.join(data_dir, filename), 'voxels')
    voxels = np.array((voxels > 0.5)).astype(float)
    scale = (24 / 32)
    if (rand_voxels != None):
        idx = np.random.randint(voxels.shape[0], size=rand_voxels)
        voxels = voxels[idx]
        saveVoxelsToMat(voxels, os.path.join(data_dir, 'samples.mat'), 'voxels')
    num_voxels = voxels.shape[0]
    new_voxel = np.zeros(shape=(num_voxels, 30, 30, 30))
    for i in range(num_voxels):
        voxel = np.squeeze(voxels[i])
        voxel = nd.zoom(voxel, (scale, scale, scale), mode='nearest', order=3)
        voxel = np.pad(voxel, 3, mode='constant', constant_values=0)
        new_voxel[i] = voxel
    new_voxel = np.array((new_voxel > 0.5)).astype(float)
    saveVoxelsToMat(new_voxel, os.path.join(data_dir, 'syn_results.mat'), 'v')
