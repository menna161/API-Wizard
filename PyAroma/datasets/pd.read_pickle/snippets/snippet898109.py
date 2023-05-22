import chainer
import h5py
import numpy as np
import pandas as pd


def __init__(self, n_frames, h5path, config_path, img_size):
    self.h5file = h5py.File(h5path, 'r')
    self.dset = self.h5file['image']
    self.conf = pd.read_pickle(config_path)
    self.ind = self.conf.index.tolist()
    self.n_frames = n_frames
    self.img_size = img_size
