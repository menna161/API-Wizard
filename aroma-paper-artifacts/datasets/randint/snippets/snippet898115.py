import chainer
import h5py
import numpy as np
import pandas as pd


def _crop_center(self, x):
    h_shift = (np.random.randint((x.shape[2] - self.img_size)) if (x.shape[2] > self.img_size) else 0)
    w_shift = (np.random.randint((x.shape[3] - self.img_size)) if (x.shape[3] > self.img_size) else 0)
    x = x[(:, :, h_shift:(h_shift + self.img_size), w_shift:(w_shift + self.img_size))]
    assert (x.shape[2] == self.img_size)
    assert (x.shape[3] == self.img_size)
    return x
