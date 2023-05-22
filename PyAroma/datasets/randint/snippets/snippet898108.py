import chainer
import numpy as np


def get_example(self, i):
    T = self.dset.shape[1]
    ot = (np.random.randint((T - self.n_frames)) if (T > self.n_frames) else 0)
    x = self.dset[(i, ot:(ot + self.n_frames))]
    return np.asarray(((x - 128.0) / 128.0), dtype=np.float32)
