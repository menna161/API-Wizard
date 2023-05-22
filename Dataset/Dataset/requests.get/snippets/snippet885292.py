import logging
import re
import sys
import os
import unittest
from contextlib import contextmanager
from io import StringIO
import tempfile
from lxml.etree import XMLSyntaxError, fromstring
from requests.exceptions import HTTPError
import mock
import premailer.premailer
from nose.tools import assert_raises, eq_, ok_
from premailer.__main__ import main
from premailer.premailer import ExternalNotFoundError, ExternalFileLoadingError, Premailer, csstext_to_pairs, merge_styles, transform
import os
import threading
import logging


@mock.patch('premailer.premailer.requests')
def test_load_external_url_no_insecure_ssl(self, mocked_requests):
    'Test premailer.premailer.Premailer._load_external_url'
    faux_response = 'This is not a response'
    faux_uri = 'https://example.com/site.css'
    mocked_requests.get.return_value = MockResponse(faux_response)
    p = premailer.premailer.Premailer('<p>A paragraph</p>', allow_insecure_ssl=False)
    r = p._load_external_url(faux_uri)
    mocked_requests.get.assert_called_once_with(faux_uri, verify=True)
    eq_(faux_response, r)
