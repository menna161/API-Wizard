import dexplo as dx
import numpy as np
from numpy import nan, array
import pytest
from dexplo.testing import assert_frame_equal, assert_array_equal


def append_multiple_new_old_arrays(self):
    df1 = self.df.append({'a': 10, 'b': np.arange(10, 15), 'h': np.arange(5), 'i': np.linspace(2.4, 20.9, 5)}, axis='columns')
    data2 = {'a': array([10, 10, 10, 10, 10]), 'b': array([10, 11, 12, 13, 14]), 'c': array([None, 'e', 'e', 'a', 'z'], dtype=object), 'd': array([False, False, True, False, True]), 'e': array([0, 20, 30, 4, 4]), 'f': array(['a', None, 'ad', None, 'ad'], dtype=object), 'g': array([2.4, 7.025, 11.65, 16.275, 20.9]), 'h': array([0, 1, 2, 3, 4]), 'i': array([2.4, 7.025, 11.65, 16.275, 20.9])}
    df2 = dx.DataFrame(data2)
    assert_frame_equal(df1, df2)
