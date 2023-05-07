import dexplo as dx
import numpy as np
from numpy import nan, array
import pytest
from dexplo.testing import assert_frame_equal


def test_abs(self):
    df1 = self.df.abs()
    df2 = dx.DataFrame({'a': array([0, 109, 1234, 603]), 'b': array([0.19185, 1.5123, nan, 122.445]), 'c': array(['b', 'b', 'g', 'a'], dtype=object), 'd': array([False, False, True, True]), 'e': array([9981, 2411, 2423, 123]), 'f': array(['', None, 'ad', 'wer'], dtype=object), 'g': array([0, 0, 0, 0]), 'h': array([nan, nan, nan, nan]), 'i': array([2, 4, 4, 2], dtype='datetime64[ns]'), 'j': array([10, 40, 10, 40], dtype='timedelta64[ns]'), 'k': array([200, 4, 5, (- 99)], dtype='datetime64[ns]'), 'l': array([20, 4, 51, 4], dtype='timedelta64[ns]')})
    assert_frame_equal(df1, df2)
    df1 = abs(self.df)
    assert_frame_equal(df1, df2)
