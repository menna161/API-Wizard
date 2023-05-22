import dexplo as dx
import numpy as np
from numpy import nan, array
import pytest
from dexplo.testing import assert_frame_equal


def test_round(self):
    df1 = self.df.round(1)
    df2 = dx.DataFrame({'a': [0, (- 109), 1234, 603], 'b': [0.2, (- 1.5), np.nan, 122.4], 'c': ['b', 'b', 'g', 'a'], 'd': [False, False, True, True], 'e': [(- 9981), 2411, 2423, (- 123)], 'f': ['', None, 'ad', 'wer'], 'g': np.zeros(4, dtype='int64'), 'h': ([np.nan] * 4), 'i': np.array([2, 4, 4, 2], dtype='datetime64[ns]'), 'j': np.array([(- 10), (- 40), 10, 40], dtype='timedelta64[ns]'), 'k': np.array([200, 4, 5, (- 99)], dtype='datetime64[ns]'), 'l': np.array([20, 4, (- 51), 4], dtype='timedelta64[ns]')})
    assert_frame_equal(df1, df2)
