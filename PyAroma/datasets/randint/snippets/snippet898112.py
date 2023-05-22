import chainer
import h5py
import numpy as np
import pandas as pd


def get_example(self, i):
    mov_info = self.conf.loc[self.ind[i]]
    length = (mov_info.end - mov_info.start)
    offset = (np.random.randint((length - self.n_frames)) if (length > self.n_frames) else 0)
    x = self.dset[(mov_info.start + offset):((mov_info.start + offset) + self.n_frames)]
    x = self._crop_center(x)
    return np.asarray(((x - 128.0) / 128.0), dtype=np.float32)
