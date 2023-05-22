import operator
import pytest
import numpy as np
from numpy.testing import assert_array_equal
from astropy.tests.helper import assert_follows_unicode_guidelines, catch_warnings
from astropy import table
from astropy import units as u
from astropy.utils.tests.test_metadata import MetaBaseTest
from astropy import conf
from inspect import currentframe, getframeinfo


def test_format(self, Column):
    'Show that the formatted output from str() works'
    from astropy import conf
    with conf.set_temp('max_lines', 8):
        c1 = Column(np.arange(2000), name='a', dtype=float, format='%6.2f')
        assert (str(c1).splitlines() == ['   a   ', '-------', '   0.00', '   1.00', '    ...', '1998.00', '1999.00', 'Length = 2000 rows'])
