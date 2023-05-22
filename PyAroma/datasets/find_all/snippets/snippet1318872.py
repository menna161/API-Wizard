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


def _parse_tbody_tr(self, table):
    from_tbody = table.select('tbody tr')
    from_root = table.find_all('tr', recursive=False)
    return (from_tbody + from_root)
