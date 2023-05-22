from __future__ import division, print_function, absolute_import, unicode_literals
import os
import re
import shutil
import logging
import requests
from itertools import product
from functools import partial
from tempfile import NamedTemporaryFile
import six
from six.moves import urllib
from .config import KPLR_ROOT
from . import mast
import astropy.io.fits as pyfits
import fitsio
import numpy as np
import matplotlib.pyplot as pl
from tornado import gen
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


def ea_request(self, table, sort=None, **params):
    '\n        Submit a request to the Exoplanet Archive API and return a dictionary.\n\n        :param table:\n            The table that you want to search.\n\n        :param **params:\n            Any other search parameters.\n\n        '
    params['table'] = table
    if (sort is not None):
        if isinstance(sort, six.string_types):
            params['order'] = sort
        else:
            params['order'] = sort[0]
            if (sort[1] == (- 1)):
                params['order'] += '+desc'
    payload = ['{0}={1}'.format(k, urllib.parse.quote_plus(v, '"\'+')) for (k, v) in params.items()]
    r = requests.get(self.ea_url, params=payload)
    r.raise_for_status()
    txt = r.text
    csv = txt.splitlines()
    columns = csv[0].split(',')
    result = []
    for line in csv[1:]:
        result.append(dict(zip(columns, line.split(','))))
    return [self._munge_dict(row) for row in result]
