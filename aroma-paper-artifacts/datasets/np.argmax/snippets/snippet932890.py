import os
import numpy as np
import torch
import random
import time
import numba as nb
import yaml
from torch.utils import data


def __getitem__(self, index):
    'Generates one sample of data'
    data = self.point_cloud_dataset[index]
    if (len(data) == 2):
        (xyz, labels) = data
    elif (len(data) == 3):
        (xyz, labels, sig) = data
        if (len(sig.shape) == 2):
            sig = np.squeeze(sig)
    else:
        raise Exception('Return invalid data tuple')
    if self.rotate_aug:
        rotate_rad = np.deg2rad((np.random.random() * 360))
        (c, s) = (np.cos(rotate_rad), np.sin(rotate_rad))
        j = np.matrix([[c, s], [(- s), c]])
        xyz[(:, :2)] = np.dot(xyz[(:, :2)], j)
    if self.flip_aug:
        flip_type = np.random.choice(4, 1)
        if (flip_type == 1):
            xyz[(:, 0)] = (- xyz[(:, 0)])
        elif (flip_type == 2):
            xyz[(:, 1)] = (- xyz[(:, 1)])
        elif (flip_type == 3):
            xyz[(:, :2)] = (- xyz[(:, :2)])
    xyz_pol = cart2polar(xyz)
    max_bound_r = np.percentile(xyz_pol[(:, 0)], 100, axis=0)
    min_bound_r = np.percentile(xyz_pol[(:, 0)], 0, axis=0)
    max_bound = np.max(xyz_pol[(:, 1:)], axis=0)
    min_bound = np.min(xyz_pol[(:, 1:)], axis=0)
    max_bound = np.concatenate(([max_bound_r], max_bound))
    min_bound = np.concatenate(([min_bound_r], min_bound))
    if self.fixed_volume_space:
        max_bound = np.asarray(self.max_volume_space)
        min_bound = np.asarray(self.min_volume_space)
    crop_range = (max_bound - min_bound)
    cur_grid_size = self.grid_size
    intervals = (crop_range / (cur_grid_size - 1))
    if (intervals == 0).any():
        print('Zero interval!')
    grid_ind = np.floor(((np.clip(xyz_pol, min_bound, max_bound) - min_bound) / intervals)).astype(np.int)
    voxel_position = np.zeros(self.grid_size, dtype=np.float32)
    dim_array = np.ones((len(self.grid_size) + 1), int)
    dim_array[0] = (- 1)
    voxel_position = ((np.indices(self.grid_size) * intervals.reshape(dim_array)) + min_bound.reshape(dim_array))
    processed_label = (np.ones(self.grid_size, dtype=np.uint8) * self.ignore_label)
    label_voxel_pair = np.concatenate([grid_ind, labels], axis=1)
    label_voxel_pair = label_voxel_pair[(np.lexsort((grid_ind[(:, 0)], grid_ind[(:, 1)], grid_ind[(:, 2)])), :)]
    processed_label = nb_process_label(np.copy(processed_label), label_voxel_pair)
    valid_label = np.zeros_like(processed_label, dtype=bool)
    valid_label[(grid_ind[(:, 0)], grid_ind[(:, 1)], grid_ind[(:, 2)])] = True
    valid_label = valid_label[::(- 1)]
    max_distance_index = np.argmax(valid_label, axis=0)
    max_distance = (max_bound[0] - (intervals[0] * max_distance_index))
    distance_feature = (np.expand_dims(max_distance, axis=2) - np.transpose(voxel_position[0], (1, 2, 0)))
    distance_feature = np.transpose(distance_feature, (1, 2, 0))
    distance_feature = ((distance_feature > 0) * (- 1.0))
    distance_feature[(grid_ind[(:, 2)], grid_ind[(:, 0)], grid_ind[(:, 1)])] = 1.0
    data_tuple = (distance_feature, processed_label)
    voxel_centers = (((grid_ind.astype(np.float32) + 0.5) * intervals) + min_bound)
    return_xyz = (xyz_pol - voxel_centers)
    return_xyz = np.concatenate((return_xyz, xyz_pol, xyz[(:, :2)]), axis=1)
    if (len(data) == 2):
        return_fea = return_xyz
    elif (len(data) == 3):
        return_fea = np.concatenate((return_xyz, sig[(..., np.newaxis)]), axis=1)
    if self.return_test:
        data_tuple += (grid_ind, labels, return_fea, index)
    else:
        data_tuple += (grid_ind, labels, return_fea)
    return data_tuple
