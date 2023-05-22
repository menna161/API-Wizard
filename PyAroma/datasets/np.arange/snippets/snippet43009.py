import dexplo as dx
import numpy as np
from numpy import nan, array
import pytest
from dexplo.testing import assert_frame_equal, assert_array_equal


def test_where_array_xy(self):
    data = {'a': [9, 10, 9, 9, 10], 'b': [0, nan, nan, 0, 1], 'c': ([''] + list('eeaz')), 'd': [False, False, True, False, True], 'e': [0, 20, 30, 4, 4], 'f': ['a', nan, 'ad', None, 'ad'], 'g': ([np.nan] * 5)}
    df = dx.DataFrame(data)
    cond = (df[(:, 'e')] > 9)
    df1 = df[(:, ['c', 'f'])].where(cond, np.arange(5), np.arange(10, 15))
    df2 = dx.DataFrame({'c': [10, 1, 2, 13, 14], 'f': [10, 1, 2, 13, 14]})
    assert_frame_equal(df1, df2)
    df1 = df[(:, ['c', 'f'])].where(cond, np.arange(5), 99)
    df2 = dx.DataFrame({'c': [99, 1, 2, 99, 99], 'f': [99, 1, 2, 99, 99]})
    assert_frame_equal(df1, df2)
    with pytest.raises(TypeError):
        df[(:, ['c', 'f'])].where(cond, np.arange(5), 'er')
    df1 = df[(:, ['c', 'f'])].where(cond, y='er')
    df2 = dx.DataFrame({'c': ['er', 'e', 'e', 'er', 'er'], 'f': ['er', None, 'ad', 'er', 'er']})
    assert_frame_equal(df1, df2)
