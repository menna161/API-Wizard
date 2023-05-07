import dexplo as dx
import numpy as np
from numpy import array, nan
import pytest
from dexplo.testing import assert_frame_equal


def test_bool_to_float(self):
    df1 = df.astype({'d': 'float'})
    df2 = dx.DataFrame({'a': [1, nan, 10, 0], 'b': ['a', 'a', 'c', 'c'], 'c': [5, 1, nan, 3], 'd': [1.0, 0, 1, nan], 'e': [3.2, nan, 1, 0], 'f': np.array([5, 10, NaTdt, 4], 'datetime64[Y]'), 'g': np.array([22, 10, NaTtd, 8], 'timedelta64[m]')})
    assert_frame_equal(df1, df2)
    df1 = dx.DataFrame({'a': [True, False, True, True], 'b': [True, False, True, nan]})
    df1 = df1.astype('float')
    df2 = dx.DataFrame({'a': [1.0, 0, 1, 1], 'b': [1.0, 0, 1, nan]})
    assert_frame_equal(df1, df2)
