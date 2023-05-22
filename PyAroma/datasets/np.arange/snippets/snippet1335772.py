import pytest
import numpy as np
from astropy import table
from astropy.table import Table, QTable
from astropy.table.table_helpers import simple_table
from astropy import units as u
from astropy.utils import console
from astropy import conf
from astropy import conf


def test_column_format_with_threshold_masked_table(self):
    from astropy import conf
    with conf.set_temp('max_lines', 8):
        t = Table([np.arange(20)], names=['a'], masked=True)
        t['a'].format = '%{0:}'
        t['a'].mask[0] = True
        t['a'].mask[(- 1)] = True
        assert (str(t['a']).splitlines() == [' a ', '---', ' --', ' %1', '...', '%18', ' --', 'Length = 20 rows'])
        t['a'].format = '{ %4.2f }'
        assert (str(t['a']).splitlines() == ['    a    ', '---------', '       --', ' { 1.00 }', '      ...', '{ 18.00 }', '       --', 'Length = 20 rows'])
