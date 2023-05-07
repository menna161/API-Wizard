import pytest
import numpy as np
from astropy import table
from astropy.table import Table, QTable
from astropy.table.table_helpers import simple_table
from astropy import units as u
from astropy.utils import console
from astropy import conf
from astropy import conf


def test_column_format_with_threshold(self, table_type):
    from astropy import conf
    with conf.set_temp('max_lines', 8):
        t = table_type([np.arange(20)], names=['a'])
        t['a'].format = '%{0:}'
        assert (str(t['a']).splitlines() == [' a ', '---', ' %0', ' %1', '...', '%18', '%19', 'Length = 20 rows'])
        t['a'].format = '{ %4.2f }'
        assert (str(t['a']).splitlines() == ['    a    ', '---------', ' { 0.00 }', ' { 1.00 }', '      ...', '{ 18.00 }', '{ 19.00 }', 'Length = 20 rows'])
