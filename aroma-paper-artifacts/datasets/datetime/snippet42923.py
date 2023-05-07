import dexplo as dx
import numpy as np
from numpy import array, nan
import pytest
from dexplo.testing import assert_frame_equal


def test_date_to_float(self):
    df1 = dx.DataFrame({'a': np.array([5, 10], 'datetime64[Y]'), 'b': np.array([22, 10], 'timedelta64[m]')})
    with pytest.raises(ValueError):
        df1.astype({'a': 'float'})
    with pytest.raises(ValueError):
        df1.astype('float')
