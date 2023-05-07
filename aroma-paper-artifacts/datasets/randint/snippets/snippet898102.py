import os
import random
import chainer
import numpy as np
import pandas as pd
from PIL import Image


def get_example(self, i):
    cols = self.conf.loc[i]
    m = random.randint(cols.start, cols.end)
    clip = Image.open(os.path.join(self.root_path, cols.path, '{:04d}.jpg'.format(m)))
    T = (clip.height // 128)
    clip = clip.resize((64, (T * 64)), Image.NEAREST)
    clip = np.asarray(clip)
    clip = clip.reshape(T, 64, 64, 3)
    ot = (np.random.randint((T - self.n_frames)) if (T > self.n_frames) else 0)
    x = clip[ot:(ot + self.n_frames)]
    x = x.transpose(0, 3, 1, 2)
    return ((x - 128.0) / 128.0).astype(np.float32)
