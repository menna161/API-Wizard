import dexplo as dx
import numpy as np
from numpy import array, nan
import pytest
from dexplo.testing import assert_frame_equal


def test_int_to_bool(self):
    df1 = df.astype({'a': 'bool', 'c': 'bool'})
    df2 = dx.DataFrame({'a': [True, nan, True, False], 'b': ['a', 'a', 'c', 'c'], 'c': [True, True, nan, True], 'd': [True, False, True, nan], 'e': [3.2, nan, 1, 0], 'f': np.array([5, 10, NaTdt, 4], 'datetime64[Y]'), 'g': np.array([22, 10, NaTtd, 8], 'timedelta64[m]')})
    assert_frame_equal(df1, df2)
    df1 = dx.DataFrame({'a': [1, 0, 10, nan], 'b': [5, 1, 14, nan]})
    df1 = df1.astype('bool')
    df2 = dx.DataFrame({'a': [True, False, True, nan], 'b': [True, True, True, nan]})
    assert_frame_equal(df1, df2)
