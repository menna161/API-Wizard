import numpy as np
import os
import h5py
import argparse
from joblib import Parallel, delayed


def sample_points_from_vox3d(voxel_model_64, dim_voxel, batch_size, d=2, sigma=0.1):
    'sample points from voxel surface\n\n    :param voxel_model_64: voxel model at 64^3 resolution\n    :param dim_voxel: target dimension of sampled points\n    :param batch_size: number of points to be sampled\n    :param d: size of neighbor window\n    :param sigma: sigma for normal distribution\n    :return:\n    '
    ori_dim = voxel_model_64.shape[0]
    multiplier = int((ori_dim // dim_voxel))
    voxel_model = np.zeros(((dim_voxel + (d * 2)), (dim_voxel + (d * 2)), (dim_voxel + (d * 2))), dtype=np.uint8)
    voxel_model_fullfill = np.zeros((dim_voxel, dim_voxel, dim_voxel), dtype=np.uint8)
    for i in range(dim_voxel):
        for j in range(dim_voxel):
            for k in range(dim_voxel):
                voxel_model_fullfill[(i, j, k)] = np.max(voxel_model_64[((i * multiplier):((i + 1) * multiplier), (j * multiplier):((j + 1) * multiplier), (k * multiplier):((k + 1) * multiplier))])
    voxel_model[(d:(d + dim_voxel), d:(d + dim_voxel), d:(d + dim_voxel))] = voxel_model_fullfill
    del voxel_model_fullfill
    bbox = find_bounding_box(voxel_model)
    exceed = 0
    sample_points = np.zeros([batch_size, 3], np.float)
    sample_values = np.zeros([batch_size, 1], np.uint8)
    batch_size_counter = 0
    voxel_model_flag = np.zeros_like(voxel_model, dtype=np.uint8)
    positive = 0
    for i in range(max((bbox[0] - d), d), min((bbox[1] + d), (dim_voxel + d))):
        for j in range(max((bbox[2] - d), d), min((bbox[3] + d), (dim_voxel + d))):
            for k in range(max((bbox[4] - d), d), min((bbox[5] + d), (dim_voxel + d))):
                if (batch_size_counter >= batch_size):
                    break
                neighbor_cube = voxel_model[((i - d):((i + d) + 1), (j - d):((j + d) + 1), (k - d):((k + d) + 1))]
                if (np.max(neighbor_cube) != np.min(neighbor_cube)):
                    sample_points[(batch_size_counter, 0)] = i
                    sample_points[(batch_size_counter, 1)] = j
                    sample_points[(batch_size_counter, 2)] = k
                    sample_values[(batch_size_counter, 0)] = voxel_model[(i, j, k)]
                    if (voxel_model[(i, j, k)] >= 1):
                        positive += 1
                    voxel_model_flag[(i, j, k)] = 1
                    batch_size_counter += 1
    positive = 0
    if (batch_size_counter >= batch_size):
        exceed += 1
        batch_size_counter = 0
        voxel_model_flag = np.zeros_like(voxel_model, dtype=np.uint8)
        for i in range(max((bbox[0] - d), d), min((bbox[1] + d), (dim_voxel + d)), 2):
            for j in range(max((bbox[2] - d), d), min((bbox[3] + d), (dim_voxel + d)), 2):
                for k in range(max((bbox[4] - d), d), min((bbox[5] + d), (dim_voxel + d)), 2):
                    if (batch_size_counter >= batch_size):
                        break
                    neighbor_cube = voxel_model[((i - d):((i + d) + 1), (j - d):((j + d) + 1), (k - d):((k + d) + 1))]
                    if (np.max(neighbor_cube) != np.min(neighbor_cube)):
                        sample_points[(batch_size_counter, 0)] = i
                        sample_points[(batch_size_counter, 1)] = j
                        sample_points[(batch_size_counter, 2)] = k
                        sample_values[(batch_size_counter, 0)] = voxel_model[(i, j, k)]
                        if (voxel_model[(i, j, k)] >= 1):
                            positive += 1
                        voxel_model_flag[(i, j, k)] = 1
                        batch_size_counter += 1
    if (batch_size_counter == 0):
        raise RuntimeError('no occupied! {}'.format(np.sum(voxel_model_64)))
    if (batch_size_counter < batch_size):
        repeat = (batch_size // batch_size_counter)
        remain = (batch_size % batch_size_counter)
        for i in range(1, repeat, 1):
            sample_points[((batch_size_counter * i):(batch_size_counter * (i + 1)), :)] = (sample_points[(:batch_size_counter, :)] + np.random.uniform(low=(- sigma), high=sigma, size=(batch_size_counter, 3)))
            sample_values[((batch_size_counter * i):(batch_size_counter * (i + 1)), :)] = sample_values[:batch_size_counter]
        if (remain > 0):
            indices = np.arange(batch_size_counter)
            np.random.shuffle(indices)
            indices = indices[:remain]
            sample_points[(- remain):] = (sample_points[indices] + np.random.uniform(low=(- sigma), high=sigma, size=(remain, 3)))
            sample_values[(- remain):] = sample_values[indices]
    sample_points = (sample_points - d)
    sample_points = np.clip(sample_points, 0, (dim_voxel - 1))
    if ((np.sum((sample_points < 0)) > 0) or (np.sum((sample_points > (dim_voxel - 1))) > 0)):
        raise RuntimeError('Out range.')
    nr_points_in_bbox = np.sum(voxel_model_flag[(bbox[0]:bbox[1], bbox[2]:bbox[3], bbox[4]:bbox[5])])
    size_bbox = (((bbox[1] - bbox[0]) * (bbox[3] - bbox[2])) * (bbox[5] - bbox[4]))
    bbox_ratio = (nr_points_in_bbox / size_bbox)
    return (sample_points, sample_values, exceed, bbox_ratio)
