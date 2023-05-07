import dexplo as dx
import numpy as np
from numpy import nan, array
import pytest
from dexplo.testing import assert_frame_equal


def test_min_vertical(self):
    df1 = self.df.select_dtypes(exclude='str').min()
    df2 = dx.DataFrame({'a': [0], 'b': [0.0], 'd': [0], 'e': [0], 'g': [0], 'h': [np.nan], 'i': np.array([2], dtype='datetime64[ns]'), 'j': np.array([(- 12)], dtype='timedelta64[ns]'), 'k': np.array([4], dtype='datetime64[ns]'), 'l': np.array([4], dtype='timedelta64[ns]')})
    assert_frame_equal(df1, df2)
    df1 = self.df.min()
    df2 = dx.DataFrame({'a': [0], 'b': [0.0], 'c': [''], 'd': [0], 'e': [0], 'f': [''], 'g': [0], 'h': [np.nan], 'i': np.array([2], dtype='datetime64[ns]'), 'j': np.array([(- 12)], dtype='timedelta64[ns]'), 'k': np.array([4], dtype='datetime64[ns]'), 'l': np.array([4], dtype='timedelta64[ns]')})
    assert_frame_equal(df1, df2)
