from __future__ import unicode_literals
import base64
import binascii
import calendar
import codecs
import contextlib
import ctypes
import datetime
import email.utils
import errno
import functools
import gzip
import io
import itertools
import json
import locale
import math
import operator
import os
import pipes
import platform
import random
import re
import socket
import ssl
import subprocess
import sys
import tempfile
import traceback
import xml.etree.ElementTree
import zlib
from external.compat import compat_HTMLParser, compat_basestring, compat_chr, compat_etree_fromstring, compat_html_entities, compat_html_entities_html5, compat_http_client, compat_kwargs, compat_os_name, compat_parse_qs, compat_shlex_quote, compat_socket_create_connection, compat_str, compat_struct_pack, compat_struct_unpack, compat_urllib_error, compat_urllib_parse, compat_urllib_parse_urlencode, compat_urllib_parse_urlparse, compat_urllib_parse_unquote_plus, compat_urllib_request, compat_urlparse, compat_xpath
from external.socks import ProxyType, sockssocket
import ctypes
import ctypes.wintypes
import ctypes.wintypes
import msvcrt
from zipimport import zipimporter
import fcntl
import xattr
import msvcrt


def parse_iso8601(date_str, delimiter='T', timezone=None):
    ' Return a UNIX timestamp from the given date '
    if (date_str is None):
        return None
    date_str = re.sub('\\.[0-9]+', '', date_str)
    if (timezone is None):
        (timezone, date_str) = extract_timezone(date_str)
    try:
        date_format = '%Y-%m-%d{0}%H:%M:%S'.format(delimiter)
        dt = (datetime.datetime.strptime(date_str, date_format) - timezone)
        return calendar.timegm(dt.timetuple())
    except ValueError:
        pass
