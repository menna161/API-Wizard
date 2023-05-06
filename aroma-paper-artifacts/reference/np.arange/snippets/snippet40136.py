import os
import sys
import numpy as np
import h5py
import provider


def reset(self):
    ' reset order of h5 files '
    self.file_idxs = np.arange(0, len(self.h5_files))
    if self.shuffle:
        np.random.shuffle(self.file_idxs)
    self.current_data = None
    self.current_label = None
    self.current_file_idx = 0
    self.batch_idx = 0
