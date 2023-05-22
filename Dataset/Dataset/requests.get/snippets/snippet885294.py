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
def test_load_external_url_404(self, mocked_requests):
    'Test premailer.premailer.Premailer._load_external_url'
    faux_response = 'This is not a response'
    faux_uri = 'https://example.com/site.css'
    mocked_requests.get.return_value = MockResponse(faux_response, status_code=404)
    p = premailer.premailer.Premailer('<p>A paragraph</p>')
    assert_raises(HTTPError, p._load_external_url, faux_uri)
