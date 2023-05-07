from collections import OrderedDict, UserDict
from collections.abc import Mapping
import pytest
import numpy as np
from astropy.table import Column, TableColumns, Table, MaskedColumn


@pytest.mark.usefixtures('table_type')
@pytest.mark.parametrize('copy', [False, True])
def test_init_and_ref_from_dict(table_type, copy):
    '\n    Test that initializing from a dict works for both copy=False and True and that\n    the referencing is as expected.\n    '
    x1 = np.arange(10.0)
    x2 = np.zeros(10)
    col_dict = dict([('x1', x1), ('x2', x2)])
    t = table_type(col_dict, copy=copy)
    assert (set(t.colnames) == set(['x1', 'x2']))
    assert (t['x1'].shape == (10,))
    assert (t['x2'].shape == (10,))
    t['x1'][0] = (- 200)
    t['x2'][1] = (- 100)
    if copy:
        assert (x1[0] == 0.0)
        assert (x2[1] == 0.0)
    else:
        assert (x1[0] == (- 200))
        assert (x2[1] == (- 100))
