import dexplo as dx
import numpy as np
from numpy import array, nan
import pytest
from dexplo.testing import assert_frame_equal


def test_float_to_bool(self):
    df1 = df.astype({'e': 'bool'})
    df2 = dx.DataFrame({'a': [1, nan, 10, 0], 'b': ['a', 'a', 'c', 'c'], 'c': [5, 1, nan, 3], 'd': [True, False, True, nan], 'e': [True, nan, True, False], 'f': np.array([5, 10, NaTdt, 4], 'datetime64[Y]'), 'g': np.array([22, 10, NaTtd, 8], 'timedelta64[m]')})
    assert_frame_equal(df1, df2)
    df1 = dx.DataFrame({'a': [3.2, nan, 0], 'b': [0.0, 4, 2]})
    df1 = df1.astype('bool')
    df2 = dx.DataFrame({'a': [True, nan, False], 'b': [False, True, True]})
    assert_frame_equal(df1, df2)
