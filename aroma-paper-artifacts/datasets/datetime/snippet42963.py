import dexplo as dx
import numpy as np
from numpy import array, nan
import pytest
from dexplo.testing import assert_frame_equal, assert_array_equal, assert_dict_list


def test_single_list_dt(self):
    a = [np.datetime64(x, 'ns') for x in [10, 20, 30]]
    df1 = dx.DataFrame({'a': a})
    assert_array_equal(np.array(a), df1._data['M'][(:, 0)])
    assert (df1._column_info['a'].values == ('M', 0, 0))
