import warnings
import numpy
from . import core
from astropy.table import Column
from astropy.utils.xml import writer
from copy import deepcopy
from bs4 import BeautifulSoup


def __call__(self, lines):
    '\n        Return HTML data from lines as a generator.\n        '
    for line in lines:
        if (not isinstance(line, SoupString)):
            raise TypeError('HTML lines should be of type SoupString')
        soup = line.soup
        header_elements = soup.find_all('th')
        if header_elements:
            (yield [((el.text.strip(), el['colspan']) if el.has_attr('colspan') else el.text.strip()) for el in header_elements])
        data_elements = soup.find_all('td')
        if data_elements:
            (yield [el.text.strip() for el in data_elements])
    if (len(lines) == 0):
        raise core.InconsistentTableError('HTML tables must contain data in a <table> tag')
