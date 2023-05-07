import numpy as np
from .rules import *


def _shuffle_update_order(self, n):
    self._update_order = np.arange(n)
    np.random.shuffle(self._update_order)
    self._update_order = self._update_order.tolist()
