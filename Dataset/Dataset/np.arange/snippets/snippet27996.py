import os
import shlex
import subprocess
import h5py
import numpy as np
import torch
import torch.utils.data as data


def __getitem__(self, idx):
    pt_idxs = np.arange(0, self.num_points)
    np.random.shuffle(pt_idxs)
    current_points = torch.from_numpy(self.points[(idx, pt_idxs)].copy()).float()
    current_labels = torch.from_numpy(self.labels[(idx, pt_idxs)].copy()).long()
    return (current_points, current_labels)
