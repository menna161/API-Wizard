import dexplo as dx
import numpy as np
from numpy import nan, array
import pytest
from dexplo.testing import assert_frame_equal, assert_array_equal


def test_append_one_array(self):
    df1 = self.df.append({'h': np.arange(5)}, axis='columns')
    data2 = {'a': array([9, 10, 9, 9, 10]), 'b': array([0.0, nan, nan, 0.0, 1.0]), 'c': array([None, 'e', 'e', 'a', 'z'], dtype=object), 'd': array([False, False, True, False, True]), 'e': array([0, 20, 30, 4, 4]), 'f': array(['a', None, 'ad', None, 'ad'], dtype=object), 'g': array([nan, nan, nan, nan, nan]), 'h': array([0, 1, 2, 3, 4])}
    df2 = dx.DataFrame(data2)
    assert_frame_equal(df1, df2)
