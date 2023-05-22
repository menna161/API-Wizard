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


def mast_request(self, category, adapter=None, sort=None, mission='kepler', **params):
    '\n        Submit a request to the MAST API and return a dictionary of parameters.\n\n        :param category:\n            The table that you want to search.\n\n        :param **params:\n            Any other search parameters.\n\n        '
    params['action'] = params.get('action', 'Search')
    params['outputformat'] = 'JSON'
    params['coordformat'] = 'dec'
    params['verb'] = 3
    if (sort is not None):
        if isinstance(sort, six.string_types):
            params['ordercolumn1'] = sort
        else:
            params['ordercolumn1'] = sort[0]
            if (sort[1] == (- 1)):
                params['descending1'] = 'on'
    r = requests.get(self.mast_url.format(mission, category), params=params)
    r.raise_for_status()
    if ('no rows' in r.text):
        return []
    result = r.json()
    if (adapter is None):
        return [self._munge_dict(row) for row in result]
    return [adapter(row) for row in result]
