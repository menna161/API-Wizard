from __future__ import absolute_import
from chainer import backend
from chainer import Variable
import numpy as np


def __call__(self, samples):
    samples = self._preprocess(samples)
    xp = backend.get_array_module(samples)
    n_samples = len(samples)
    if (self.size == 0):
        pass
    elif (len(self._buffer) == 0):
        self._buffer = samples
    elif (len(self._buffer) < self.size):
        self._buffer = xp.vstack((self._buffer, samples))
    else:
        random_bool = (np.random.rand(n_samples) < self.p)
        replay_indices = np.random.randint(0, len(self._buffer), size=n_samples)[random_bool]
        sample_indices = np.random.randint(0, n_samples, size=n_samples)[random_bool]
        (self._buffer[replay_indices], samples[sample_indices]) = (samples[sample_indices], self._buffer[replay_indices])
    return self._postprocess(samples)
