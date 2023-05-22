import pytest
import numpy as np


def test_np_integers(self, table_data):
    '\n        Select rows using numpy integers.  This is a regression test for a\n        py 3.3 failure mode\n        '
    t = table_data.Table(table_data.COLS)
    idxs = np.random.randint(len(t), size=2)
    item = t[idxs[1]]
