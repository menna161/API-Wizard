from __future__ import absolute_import, division, print_function, unicode_literals
import os
import pkgutil
import requests
import unittest
from mock import patch
from nose.tools import assert_equals
from .utils import fake_response
import pygenie


@patch('requests.Session.request')
def test_request_call(self, request):
    'Test request call kwargs for auth.'
    patcher = None
    if pkgutil.find_loader('eureq'):
        patcher = patch('eureq.request', check_request_auth_kwargs)
        patcher.start()
    request.side_effect = check_request_auth_kwargs
    pygenie.utils.call('http://localhost', auth_handler=pygenie.auth.AuthHandler(conf=self.conf))
    if patcher:
        patcher.stop()
