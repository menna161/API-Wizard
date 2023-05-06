import os
import sys
from eulerangles import euler2mat
import numpy as np
from plyfile import PlyData, PlyElement
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.pyplot as pyplot


def point_cloud_label_to_surface_voxel_label(point_cloud, label, res=0.0484):
    coordmax = np.max(point_cloud, axis=0)
    coordmin = np.min(point_cloud, axis=0)
    nvox = np.ceil(((coordmax - coordmin) / res))
    vidx = np.ceil(((point_cloud - coordmin) / res))
    vidx = ((vidx[(:, 0)] + (vidx[(:, 1)] * nvox[0])) + ((vidx[(:, 2)] * nvox[0]) * nvox[1]))
    uvidx = np.unique(vidx)
    if (label.ndim == 1):
        uvlabel = [np.argmax(np.bincount(label[(vidx == uv)].astype(np.uint32))) for uv in uvidx]
    else:
        assert (label.ndim == 2)
    uvlabel = np.zeros(len(uvidx), label.shape[1])
    for i in range(label.shape[1]):
        uvlabel[(:, i)] = np.array([np.argmax(np.bincount(label[((vidx == uv), i)].astype(np.uint32))) for uv in uvidx])
    return (uvidx, uvlabel, nvox)
