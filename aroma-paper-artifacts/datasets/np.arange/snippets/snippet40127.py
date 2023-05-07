import os
import os.path
import json
import numpy as np
import sys
import provider
import time


def reset(self):
    self.idxs = np.arange(0, len(self.datapath))
    if self.shuffle:
        np.random.shuffle(self.idxs)
    self.num_batches = (((len(self.datapath) + self.batch_size) - 1) // self.batch_size)
    self.batch_idx = 0
