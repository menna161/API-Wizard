import numpy as np
import os
import unittest
from tensorpack.dataflow import HDF5Serializer, LMDBSerializer, NumpySerializer, TFRecordSerializer
from tensorpack.dataflow.base import DataFlow


def reset_state(self):
    np.random.seed(self.seed)
    for _ in range(self._size):
        label = np.random.randint(low=0, high=10)
        img = np.random.randn(28, 28, 3)
        self.cache.append([label, img])
