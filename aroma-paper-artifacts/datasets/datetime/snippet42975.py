import dexplo as dx
import numpy as np
from numpy import array, nan
import pytest
from dexplo.testing import assert_frame_equal, assert_array_equal, assert_dict_list


def test_array_dt(self):
    a = np.array([10, 20, 30], dtype='datetime64[ns]')
    b = np.array([100, 200, 300], dtype='datetime64[ns]')
    arr = np.column_stack((a, b))
    df1 = dx.DataFrame({'a': a, 'b': b})
    assert_array_equal(arr, df1._data['M'])
    assert (df1._column_info['a'].values == ('M', 0, 0))
    assert (df1._column_info['b'].values == ('M', 1, 1))
