from torch.utils.data import Dataset
import torch
import numpy as np
import os
import json
import random
from dataset.data_utils import collect_data_id, load_from_hdf5_by_part


def __getitem__(self, index):
    (shape_path, part_idx) = self.parts_info[index]
    (n_parts, parts_voxel, data_points, data_values) = load_from_hdf5_by_part(shape_path, part_idx, self.resolution)
    if ((not self.all_points) and (len(data_points) > self.points_batch_size)):
        indices = np.arange(len(data_points))
        random.shuffle(indices)
        indices = indices[:self.points_batch_size]
        data_points = data_points[indices]
        data_values = data_values[indices]
    batch_voxels = torch.tensor(parts_voxel.astype(np.float), dtype=torch.float32).unsqueeze(0)
    batch_points = torch.tensor(data_points, dtype=torch.float32)
    batch_values = torch.tensor(data_values, dtype=torch.float32)
    return {'vox3d': batch_voxels, 'points': batch_points, 'values': batch_values, 'n_parts': n_parts, 'part_idx': part_idx, 'path': shape_path}
