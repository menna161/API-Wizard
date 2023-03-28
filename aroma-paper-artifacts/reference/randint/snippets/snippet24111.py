from os.path import os
import numpy as np
import contextlib
import pickle
import os
import os
from six.moves import urllib
import shutil
import os
from six.moves import urllib
import tarfile


def next(self, batch_size=None):
    if (batch_size is None):
        batch_size = self.batch_size
    end = (self.current + batch_size)
    images = self.images[self.idxs[self.current:end]].copy()
    labels = self.labels[self.idxs[self.current:end]].copy()
    self.current = end
    if ((self.current + batch_size) > self.idxs.size):
        self._reset()
    if self.augmented_shift:
        for i in range(batch_size):
            padded = np.pad(images[i], ((0, 0), (4, 4), (4, 4)), mode='constant')
            corner = (np.random.randint(9), np.random.randint(9))
            images[i] = padded[:, corner[0]:(corner[0] + 32), corner[1]:(corner[1] + 32)]
    if self.augmented_flip:
        for i in range(batch_size):
            if (np.random.rand() < 0.5):
                images[i] = images[i, :, :, ::(- 1)]
    return (images, labels)
