import os
import pickle
import sys
import numpy as np


def __getitem__(self, index):
    point_set = self.data[index]
    labels = self.labels[index]
    n = point_set.shape[0]
    if (self.npoints < n):
        ixs = np.random.choice(n, self.npoints, replace=False)
    elif (self.npoints == n):
        ixs = np.arange(self.npoints)
    else:
        ixs = np.random.choice(n, self.npoints, replace=True)
    tmp = point_set[(ixs, :)]
    point_set = (tmp[(:, self.columns)] / self.scale[self.columns])
    semantic_seg = np.zeros(self.npoints, dtype='int32')
    for i in range(self.npoints):
        semantic_seg[i] = self.compressed_label_map[labels[ixs[i]]]
    sample_weight = self.labelweights[semantic_seg]
    return (point_set, semantic_seg, sample_weight)
