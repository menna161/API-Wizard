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


def test_to_pandas_index(self):
    import pandas as pd
    row_index = pd.RangeIndex(0, 2, 1)
    tm_index = pd.DatetimeIndex(['1998-01-01', '2002-01-01'], dtype='datetime64[ns]', name='tm', freq=None)
    tm = Time([1998, 2002], format='jyear')
    x = [1, 2]
    t = table.QTable([tm, x], names=['tm', 'x'])
    tp = t.to_pandas()
    assert np.all((tp.index == row_index))
    tp = t.to_pandas(index='tm')
    assert np.all((tp.index == tm_index))
    t.add_index('tm')
    tp = t.to_pandas()
    assert np.all((tp.index == tm_index))
    assert t['tm'].info.indices
    tp = t.to_pandas(index=True)
    assert np.all((tp.index == tm_index))
    tp = t.to_pandas(index=False)
    assert np.all((tp.index == row_index))
    with pytest.raises(ValueError) as err:
        t.to_pandas(index='not a column')
    assert ('index must be None, False' in str(err.value))
