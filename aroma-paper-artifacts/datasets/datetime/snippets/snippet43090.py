import dexplo as dx
import numpy as np
from numpy import nan, array
import pytest
from dexplo.testing import assert_frame_equal


def test_mode_high(self):
    df1 = self.df1.select_dtypes(exclude='str').mode(keep='high')
    df2 = dx.DataFrame({'a': array([6]), 'b': array([2.0]), 'd': array([True]), 'e': array([24]), 'g': array([0]), 'h': array([nan]), 'i': array(['1970-01-01T00:00:00.000000004'], dtype='datetime64[ns]'), 'j': array([40], dtype='timedelta64[ns]'), 'k': array(['1970-01-01T00:00:00.000000200'], dtype='datetime64[ns]'), 'l': array([4], dtype='timedelta64[ns]')})
    assert_frame_equal(df1, df2)
    df1 = self.df1.select_dtypes('number').mode(keep='high', axis='columns')
    df2 = dx.DataFrame({'mode': array([0.0, 0.0, 24.0, 0.0])})
    assert_frame_equal(df1, df2)
