from __future__ import unicode_literals
from __future__ import absolute_import, division, print_function
from urllib.parse import urlparse, urljoin, urlsplit, urlunsplit, quote, unquote
from urllib.request import urlopen, Request, pathname2url
from urllib.error import HTTPError
from urlparse import urlparse, urljoin, urlsplit, urlunsplit
from urllib2 import urlopen, Request, HTTPError
from urllib import quote, unquote, pathname2url


def isoformat_space(datetime):
    '\n    Return ISO-formatted date with space to separate date and time.\n    '
    return datetime.isoformat(str_space)
