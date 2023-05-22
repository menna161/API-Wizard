from datetime import date
from itertools import count
import pytest
import numpy as np
from astropy._erfa import DJM0
from astropy.time import Time, TimeFormat
from astropy.time.utils import day_frac


@pytest.mark.parametrize('thing', [1, 1.0, np.longdouble(1), 1j, 'foo', b'foo', Time(5, format='mjd'), (lambda : 7), np.datetime64('2005-02-25'), date(2006, 2, 25)])
def test_custom_format_can_return_any_scalar(custom_format_name, thing):

    class Custom(TimeFormat):
        name = custom_format_name

        def set_jds(self, val, val2):
            (self.jd1, self.jd2) = (2.0, 0.0)

        @property
        def value(self):
            return np.array(thing)
    assert (type(getattr(Time(5, format=custom_format_name), custom_format_name)) == type(thing))
    assert np.all((getattr(Time(5, format=custom_format_name), custom_format_name) == thing))
