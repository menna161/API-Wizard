from datetime import date
from itertools import count
import pytest
import numpy as np
from astropy._erfa import DJM0
from astropy.time import Time, TimeFormat
from astropy.time.utils import day_frac


@pytest.mark.parametrize('jd1, jd2', [('foo', None), (np.arange(3), np.arange(4)), ('foo', 'bar'), (1j, 2j), pytest.param(np.longdouble(3), np.longdouble(5), marks=pytest.mark.skipif((np.longdouble().itemsize == np.dtype(float).itemsize), reason='long double == double on this platform')), ({1: 2}, {3: 4}), ({1, 2}, {3, 4}), ([1, 2], [3, 4]), ((lambda : 4), (lambda : 7)), (np.arange(3), np.arange(4))])
def test_custom_format_cannot_make_bogus_jd1(custom_format_name, jd1, jd2):

    class Custom(TimeFormat):
        name = custom_format_name

        def set_jds(self, val, val2):
            (self.jd1, self.jd2) = (jd1, jd2)

        @property
        def value(self):
            return (self.jd1 + self.jd2)
    with pytest.raises((ValueError, TypeError)):
        Time(5, format=custom_format_name)
