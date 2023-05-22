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


def test_set_new_col_existing_table(self, table_types):
    'Create a new column in an existing table using the item access syntax'
    self._setup(table_types)
    t = table_types.Table([self.a])
    t['bb'] = self.b
    assert np.all((t['bb'] == self.b))
    assert (t.colnames == ['a', 'bb'])
    assert (t['bb'].meta == self.b.meta)
    assert (t['bb'].format == self.b.format)
    t['c'] = t['a']
    assert np.all((t['c'] == t['a']))
    assert (t.colnames == ['a', 'bb', 'c'])
    assert (t['c'].meta == t['a'].meta)
    assert (t['c'].format == t['a'].format)
    t['d'] = table_types.Column(np.arange(12).reshape(3, 2, 2))
    assert (t['d'].shape == (3, 2, 2))
    assert (t['d'][(0, 0, 1)] == 1)
    t['e'] = ['hello', 'the', 'world']
    assert np.all((t['e'] == np.array(['hello', 'the', 'world'])))
    t['e'] = ['world', 'hello', 'the']
    assert np.all((t['e'] == np.array(['world', 'hello', 'the'])))
    t['f'] = 10
    assert np.all((t['f'] == 10))
    t['g'] = (np.array([1, 2, 3]) * u.m)
    assert np.all((t['g'].data == np.array([1, 2, 3])))
    assert (t['g'].unit == u.m)
    t['g'] = (3 * u.m)
    assert np.all((t['g'].data == 3))
    assert (t['g'].unit == u.m)
