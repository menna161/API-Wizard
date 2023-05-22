import pytest
import numpy as np
from astropy.table.sorted_array import SortedArray
from astropy.table.table import Table


def test_wide_array(wide_array):
    first_row = wide_array[:1].data
    assert np.all((first_row == Table([[x] for x in np.arange(100)])))
