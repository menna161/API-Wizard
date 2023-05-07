import dexplo as dx
import numpy as np
from numpy import array, nan
import pytest
from dexplo.testing import assert_frame_equal, assert_array_equal, assert_dict_list


def test_all(self):
    assert_array_equal(np.array(a), df_mix._data['i'][(:, 0)])
    assert_array_equal(np.array(b), df_mix._data['f'][(:, 0)])
    a1 = array([1, 2, 3, 4, 5, 6, 7, 8], dtype='uint32')
    assert_array_equal(a1, df_mix._data['S'][(:, 0)])
    assert_array_equal(np.array(d).astype('int8'), df_mix._data['b'][(:, 0)])
    assert_array_equal(np.array(e, dtype='datetime64[ns]'), df_mix._data['M'][(:, 0)])
    assert_array_equal(np.array(f, dtype='timedelta64[ns]'), df_mix._data['m'][(:, 0)])
    assert (df_mix._column_info['a'].values == ('i', 0, 0))
    assert (df_mix._column_info['b'].values == ('f', 0, 1))
    assert (df_mix._column_info['c'].values == ('S', 0, 2))
    assert (df_mix._column_info['d'].values == ('b', 0, 3))
    assert (df_mix._column_info['e'].values == ('M', 0, 4))
    assert (df_mix._column_info['f'].values == ('m', 0, 5))
