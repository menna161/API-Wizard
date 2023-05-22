from distutils.version import LooseVersion
import numbers
import os
import re
import pandas.compat as compat
from pandas.compat import binary_type, iteritems, lmap, lrange, raise_with_traceback, string_types, u
from pandas.errors import AbstractMethodError, EmptyDataError
from pandas.core.dtypes.common import is_list_like
from pandas import Series
from pandas.io.common import _is_url, _validate_header_arg, urlopen
from pandas.io.formats.printing import pprint_thing
from pandas.io.parsers import TextParser
import bs4
import lxml
import html5lib
from bs4 import SoupStrainer
from bs4 import BeautifulSoup
from lxml.html import parse, fromstring, HTMLParser
from lxml.etree import XMLSyntaxError
import bs4


def _parse_tables(self, doc, match, attrs):
    element_name = self._strainer.name
    tables = doc.find_all(element_name, attrs=attrs)
    if (not tables):
        raise ValueError('No tables found')
    result = []
    unique_tables = set()
    tables = self._handle_hidden_tables(tables, 'attrs')
    for table in tables:
        if self.displayed_only:
            for elem in table.find_all(style=re.compile('display:\\s*none')):
                elem.decompose()
        if ((table not in unique_tables) and (table.find(text=match) is not None)):
            result.append(table)
        unique_tables.add(table)
    if (not result):
        raise ValueError('No tables found matching pattern {patt!r}'.format(patt=match.pattern))
    return result
