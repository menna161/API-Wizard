from collections import OrderedDict
import pytest
import numpy as np
from astropy.tests.helper import catch_warnings
from astropy.table import Table, QTable, TableMergeError, Column, MaskedColumn
from astropy.table.operations import _get_out_class
from astropy import units as u
from astropy.utils import metadata
from astropy.utils.metadata import MergeConflictError
from astropy import table
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy.io.misc.asdf.tags.helpers import skycoord_equal


def test_mixin_functionality(self, mixin_cols):
    col = mixin_cols['m']
    cls_name = type(col).__name__
    len_col = len(col)
    idx = np.arange(len_col)
    t1 = table.QTable([idx, col], names=['idx', 'm1'])
    t2 = table.QTable([idx, col], names=['idx', 'm2'])
    t1 = t1[[0, 1, 3]]
    t2 = t2[[0, 2, 3]]
    out = table.join(t1, t2, join_type='inner')
    assert (len(out) == 2)
    assert (out['m2'].__class__ is col.__class__)
    assert np.all((out['idx'] == [0, 3]))
    if (cls_name == 'SkyCoord'):
        assert skycoord_equal(out['m1'], col[[0, 3]])
        assert skycoord_equal(out['m2'], col[[0, 3]])
    else:
        assert np.all((out['m1'] == col[[0, 3]]))
        assert np.all((out['m2'] == col[[0, 3]]))
    if (cls_name == 'Time'):
        out = table.join(t1, t2, join_type='left')
        assert (len(out) == 3)
        assert np.all((out['idx'] == [0, 1, 3]))
        assert np.all((out['m1'] == t1['m1']))
        assert np.all((out['m2'] == t2['m2']))
        assert np.all((out['m1'].mask == [False, False, False]))
        assert np.all((out['m2'].mask == [False, True, False]))
        out = table.join(t1, t2, join_type='right')
        assert (len(out) == 3)
        assert np.all((out['idx'] == [0, 2, 3]))
        assert np.all((out['m1'] == t1['m1']))
        assert np.all((out['m2'] == t2['m2']))
        assert np.all((out['m1'].mask == [False, True, False]))
        assert np.all((out['m2'].mask == [False, False, False]))
        out = table.join(t1, t2, join_type='outer')
        assert (len(out) == 4)
        assert np.all((out['idx'] == [0, 1, 2, 3]))
        assert np.all((out['m1'] == col))
        assert np.all((out['m2'] == col))
        assert np.all((out['m1'].mask == [False, False, True, False]))
        assert np.all((out['m2'].mask == [False, True, False, False]))
    else:
        for join_type in ('outer', 'left', 'right'):
            with pytest.raises(NotImplementedError) as err:
                table.join(t1, t2, join_type='outer')
            assert (('join requires masking' in str(err.value)) or ('join unavailable' in str(err.value)))
