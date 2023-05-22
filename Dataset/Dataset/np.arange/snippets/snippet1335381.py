import pytest
import numpy as np
from astropy.table.sorted_array import SortedArray
from astropy.table.table import Table


@pytest.fixture
def wide_array():
    t = Table([([x] * 10) for x in np.arange(100)])
    return SortedArray(t, t['col0'].copy())
