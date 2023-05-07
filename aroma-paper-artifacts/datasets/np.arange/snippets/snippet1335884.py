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


def test_reverse_big(self, table_types):
    x = np.arange(10000)
    y = (x + 1)
    t = table_types.Table([x, y], names=('x', 'y'))
    t.reverse()
    assert np.all((t['x'] == x[::(- 1)]))
    assert np.all((t['y'] == y[::(- 1)]))
