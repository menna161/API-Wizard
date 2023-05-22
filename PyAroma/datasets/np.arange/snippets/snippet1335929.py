import gc
import sys
import copy
from io import StringIO
from collections import OrderedDict
import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
from astropy.io import fits
from astropy.table import Table, QTable, MaskedColumn, TableReplaceWarning
from astropy.tests.helper import assert_follows_unicode_guidelines, ignore_warnings, catch_warnings
from astropy.coordinates import SkyCoord
from astropy.utils.data import get_pkg_data_filename
from astropy import table
from astropy import units as u
from astropy.time import Time, TimeDelta
from .conftest import MaskedTable, MIXIN_COLS
from astropy.utils.tests.test_metadata import MetaBaseTest
import pandas
import pandas as pd
from inspect import currentframe, getframeinfo


def test_insert_table_row(self, table_types):
    '\n        Light testing of Table.insert_row() method.  The deep testing is done via\n        the add_row() tests which calls insert_row(index=len(self), ...), so\n        here just test that the added index parameter is handled correctly.\n        '
    self._setup(table_types)
    row = (10, 40.0, 'x', [10, 20])
    for index in range((- 3), 4):
        indices = np.insert(np.arange(3), index, 3)
        t = table_types.Table([self.a, self.b, self.c, self.d])
        t2 = t.copy()
        t.add_row(row)
        t2.insert_row(index, row)
        for name in t.colnames:
            if (t[name].dtype.kind == 'f'):
                assert np.allclose(t[name][indices], t2[name])
            else:
                assert np.all((t[name][indices] == t2[name]))
    for index in ((- 4), 4):
        t = table_types.Table([self.a, self.b, self.c, self.d])
        with pytest.raises(IndexError):
            t.insert_row(index, row)
