import dexplo as dx
import numpy as np
from numpy import array, nan
import pytest
from dexplo.testing import assert_frame_equal


def test_int_to_str(self):
    df1 = df.astype({'a': 'str'})
    df2 = dx.DataFrame({'a': ['1', nan, '10', '0'], 'b': ['a', 'a', 'c', 'c'], 'c': [5, 1, nan, 3], 'd': [True, False, True, nan], 'e': [3.2, nan, 1, 0], 'f': np.array([5, 10, NaTdt, 4], 'datetime64[Y]'), 'g': np.array([22, 10, NaTtd, 8], 'timedelta64[m]')})
    assert_frame_equal(df1, df2)
    df1 = df[(:, ['a', 'c'])].astype('str')
    df2 = dx.DataFrame({'a': ['1', nan, '10', '0'], 'c': ['5', '1', nan, '3']})
    assert_frame_equal(df1, df2)