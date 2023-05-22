import pytest
import numpy as np
import numpy.ma as ma
from astropy.table import Column, MaskedColumn, Table, QTable
from astropy.table.column import BaseColumn
from astropy.tests.helper import catch_warnings
from astropy.time import Time
import astropy.units as u


def test_setting_from_masked_column():
    'Test issue in #2997'
    mask_b = np.array([True, True, False, False])
    for select in (mask_b, slice(0, 2)):
        t = Table(masked=True)
        t['a'] = Column([1, 2, 3, 4])
        t['b'] = MaskedColumn([11, 22, 33, 44], mask=mask_b)
        t['c'] = MaskedColumn([111, 222, 333, 444], mask=[True, False, True, False])
        t['b'][select] = t['c'][select]
        assert (t['b'][1] == t[1]['b'])
        assert (t['b'][0] is np.ma.masked)
        assert (t['b'][1] == 222)
        assert (t['b'][2] == 33)
        assert (t['b'][3] == 44)
        assert np.all((t['b'].mask == t.mask['b']))
        mask_before_add = t.mask.copy()
        t['d'] = np.arange(len(t))
        assert np.all((t.mask['b'] == mask_before_add['b']))
