import numpy as np


def get_best_frequency(self, fid=None):
    if (fid is None):
        best_idx = np.argmax(self.per)
    else:
        best_idx = np.argmax(self.per_single_band[fid])
    return self.freq[best_idx]
