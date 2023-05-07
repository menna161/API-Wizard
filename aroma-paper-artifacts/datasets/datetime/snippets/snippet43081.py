import dexplo as dx
import numpy as np
from numpy import nan, array
import pytest
from dexplo.testing import assert_frame_equal


def test_max_vertical(self):
    df1 = self.df.select_dtypes(exclude='str').max()
    df2 = dx.DataFrame({'a': [6], 'b': [1.5], 'd': [1], 'e': [30], 'g': [0], 'h': [np.nan], 'i': np.array([5], dtype='datetime64[ns]'), 'j': np.array([40], dtype='timedelta64[ns]'), 'k': np.array([200], dtype='datetime64[ns]'), 'l': np.array([51], dtype='timedelta64[ns]')})
    assert_frame_equal(df1, df2)
    df1 = self.df.max()
    df2 = dx.DataFrame({'a': [6], 'b': [1.5], 'c': ['g'], 'd': [1], 'e': [30], 'f': ['ad'], 'g': [0], 'h': [np.nan], 'i': np.array([5], dtype='datetime64[ns]'), 'j': np.array([40], dtype='timedelta64[ns]'), 'k': np.array([200], dtype='datetime64[ns]'), 'l': np.array([51], dtype='timedelta64[ns]')})
    assert_frame_equal(df1, df2)
