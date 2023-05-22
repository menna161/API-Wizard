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


def fetch(self, clobber=False):
    '\n        Download the data file from the server and save it locally. The local\n        file will be saved in the directory specified by the ``data_root``\n        property of the API.\n\n        :param clobber:\n            Should an existing local file be overwritten? (default: False)\n\n        '
    filename = self.filename
    if (self.cache_exists and (not clobber)):
        logging.info("Found local file: '{0}'".format(filename))
        return self
    url = self.url
    logging.info("Downloading file from: '{0}'".format(url))
    r = requests.get(url)
    r.raise_for_status()
    return self._save_fetched_file(r.content)
