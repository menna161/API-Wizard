import os
import os.path as osp
import shlex
import shutil
import subprocess
import lmdb
import msgpack_numpy
import numpy as np
import torch
import torch.utils.data as data
import tqdm
from torchvision import transforms
import data_utils as d_utils


def __getitem__(self, idx):
    if (self._lmdb_env is None):
        self._lmdb_env = lmdb.open(self._lmdb_file, map_size=(1 << 36), readonly=True, lock=False)
    with self._lmdb_env.begin(buffers=True) as txn:
        ele = msgpack_numpy.unpackb(txn.get(str(idx).encode()), raw=False)
    point_set = ele['pc']
    pt_idxs = np.arange(0, self.num_points)
    np.random.shuffle(pt_idxs)
    point_set = point_set[(pt_idxs, :)]
    point_set[(:, 0:3)] = pc_normalize(point_set[(:, 0:3)])
    if (self.transforms is not None):
        point_set = self.transforms(point_set)
    return (point_set, ele['lbl'])
