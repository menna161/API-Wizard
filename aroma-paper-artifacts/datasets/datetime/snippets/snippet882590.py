import torch
from torch import Tensor
from torch.utils import data
import pandas as pd
import numpy as np
import datetime as dt
import os
import json


def __getitem__(self, item):
    '\n        Returns a Pixel-Set sequence tensor with its pixel mask and optional additional features.\n        For each item npixel pixels are randomly dranw from the available pixels.\n        If the total number of pixel is too small one arbitrary pixel is repeated. The pixel mask keeps track of true\n        and repeated pixels.\n        Returns:\n              (Pixel-Set, Pixel-Mask) or ((Pixel-Set, Pixel-Mask), Extra-features) with:\n                Pixel-Set: Sequence_length x Channels x npixel\n                Pixel-Mask : Sequence_length x npixel\n                Extra-features : Sequence_length x Number of additional features\n\n        '
    x0 = np.load(os.path.join(self.folder, 'DATA', '{}.npy'.format(self.pid[item])))
    y = self.target[item]
    if (x0.shape[(- 1)] > self.npixel):
        idx = np.random.choice(list(range(x0.shape[(- 1)])), size=self.npixel, replace=False)
        x = x0[(:, :, idx)]
        mask = np.ones(self.npixel)
    elif (x0.shape[(- 1)] < self.npixel):
        if (x0.shape[(- 1)] == 0):
            x = np.zeros((*x0.shape[:2], self.npixel))
            mask = np.zeros(self.npixel)
            mask[0] = 1
        else:
            x = np.zeros((*x0.shape[:2], self.npixel))
            x[(:, :, :x0.shape[(- 1)])] = x0
            x[(:, :, x0.shape[(- 1)]:)] = np.stack([x[(:, :, 0)] for _ in range(x0.shape[(- 1)], x.shape[(- 1)])], axis=(- 1))
            mask = np.array(([1 for _ in range(x0.shape[(- 1)])] + [0 for _ in range(x0.shape[(- 1)], self.npixel)]))
    else:
        x = x0
        mask = np.ones(self.npixel)
    if (self.norm is not None):
        (m, s) = self.norm
        m = np.array(m)
        s = np.array(s)
        if (len(m.shape) == 0):
            x = ((x - m) / s)
        elif (len(m.shape) == 1):
            x = ((x.swapaxes(1, 2) - m) / s)
            x = x.swapaxes(1, 2)
        elif (len(m.shape) == 2):
            x = np.rollaxis(x, 2)
            x = ((x - m) / s)
            x = np.swapaxes(np.rollaxis(x, 1), 1, 2)
    x = x.astype('float')
    if (self.jitter is not None):
        (sigma, clip) = self.jitter
        x = (x + np.clip((sigma * np.random.randn(*x.shape)), ((- 1) * clip), clip))
    mask = np.stack([mask for _ in range(x.shape[0])], axis=0)
    data = (Tensor(x), Tensor(mask))
    if (self.extra_feature is not None):
        ef = ((self.extra[str(self.pid[item])] - self.extra_m) / self.extra_s)
        ef = torch.from_numpy(ef).float()
        ef = torch.stack([ef for _ in range(data[0].shape[0])], dim=0)
        data = (data, ef)
    if self.return_id:
        return (data, torch.from_numpy(np.array(y, dtype=int)), self.pid[item])
    else:
        return (data, torch.from_numpy(np.array(y, dtype=int)))
