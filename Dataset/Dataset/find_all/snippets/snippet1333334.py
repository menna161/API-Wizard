import warnings
import numpy
from . import core
from astropy.table import Column
from astropy.utils.xml import writer
from copy import deepcopy
from bs4 import BeautifulSoup


def process_lines(self, lines):
    '\n        Convert the given input into a list of SoupString rows\n        for further processing.\n        '
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        raise core.OptionalTableImportError('BeautifulSoup must be installed to read HTML tables')
    if ('parser' not in self.html):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', '.*no parser was explicitly specified.*')
            soup = BeautifulSoup('\n'.join(lines))
    else:
        soup = BeautifulSoup('\n'.join(lines), self.html['parser'])
    tables = soup.find_all('table')
    for (i, possible_table) in enumerate(tables):
        if identify_table(possible_table, self.html, (i + 1)):
            table = possible_table
            break
    else:
        if isinstance(self.html['table_id'], int):
            err_descr = 'number {}'.format(self.html['table_id'])
        else:
            err_descr = "id '{}'".format(self.html['table_id'])
        raise core.InconsistentTableError(f'ERROR: HTML table {err_descr} not found')
    soup_list = [SoupString(x) for x in table.find_all('tr')]
    return soup_list
