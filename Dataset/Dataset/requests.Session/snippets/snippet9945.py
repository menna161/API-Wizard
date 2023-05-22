from __future__ import absolute_import, unicode_literals, print_function
import os
import re
import sys
import json
import base64
import struct
import logging
import collections
from contextlib import contextmanager
import requests
import requests_cache
from addict import Dict as AttrDict
from rudiments.reamed import click
from .. import config
from .. import __version__ as version
from .._compat import text_type, urlparse, urlunparse, parse_qs, urlencode, unquote_plus
import pprint
import http.client as http_client
import httplib as http_client


def __init__(self, endpoint=None, session=None):
    self.log = logging.getLogger('cfapi')
    self.base_url = (endpoint or os.environ.get('CONFLUENCE_BASE_URL'))
    assert self.base_url, 'You MUST set the CONFLUENCE_BASE_URL environment variable!'
    self.base_url = self.base_url.rstrip('/')
    if (logging.getLogger('requests').getEffectiveLevel() <= logging.DEBUG):
        try:
            import http.client as http_client
        except ImportError:
            import httplib as http_client
        http_client.HTTPConnection.debuglevel = 1
    self.session = (session or requests.Session())
    self.session.headers['User-Agent'] = '{}/{} [{}]'.format(self.UA_NAME, version, requests.utils.default_user_agent())
    self.cached_session = requests_cache.CachedSession(cache_name=config.cache_file(type(self).__name__), expire_after=self.CACHE_EXPIRATION)
    self.cached_session.headers['User-Agent'] = self.session.headers['User-Agent']
