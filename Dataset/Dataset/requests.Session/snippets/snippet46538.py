from __future__ import absolute_import, division, print_function, unicode_literals
import datetime
import json
import logging
import pkg_resources
import re
import six
import socket
import sys
import time
import uuid
from functools import wraps
import requests
from .auth import AuthHandler
from requests.exceptions import Timeout, ConnectionError
from .exceptions import GenieHTTPError


def call(url, method='get', headers=None, raise_not_status=None, none_on_404=False, auth_handler=None, failure_codes=None, attempts=7, backoff=5, *args, **kwargs):
    "\n    Wrap HTTP request calls to the Genie server.\n\n    The request header will be updated to include 'user-agent'. If headers are\n    passed in with 'user-agent', it will be overwritten.\n\n    Args:\n        method (str): the HTTP method to make\n        headers (dict): headers to pass in during the request\n        raise_not_status (int): raise GenieHTTPError if this status is not\n            returned by genie.\n        none_on_404 (bool): return None if a 404 if returned instead of raising\n            GenieHTTPError (will not retry requests with 404 response).\n        failure_codes (list, optional): list of status codes to break retries and\n            return Response.\n    "
    failure_codes = (failure_codes or list())
    assert isinstance(failure_codes, (list, int)), 'failure_codes should be an int or list of ints'
    if isinstance(failure_codes, int):
        failure_codes = [failure_codes]
    failure_codes = [str(f) for f in failure_codes]
    if (none_on_404 and ('404' not in failure_codes)):
        failure_codes.append('404')
    auth_handler = (auth_handler or AuthHandler())
    headers = (USER_AGENT_HEADER if (headers is None) else dict(headers, **USER_AGENT_HEADER))
    logger.debug('"%s %s"', method.upper(), url)
    logger.debug('headers: %s', headers)
    errors = list()
    session = requests.Session()
    adapters = (kwargs.pop('session_adapters', None) or {})
    for (m, adpt) in adapters.items():
        session.mount(m, adpt)
    for i in range(attempts):
        try:
            resp = session.request(method, *args, url=url, headers=headers, auth=auth_handler.auth, **kwargs)
            if ((int((resp.status_code / 100)) == 2) or (str(resp.status_code) in failure_codes)):
                break
        except (ConnectionError, Timeout, socket.timeout) as err:
            errors.append(err)
            resp = None
        if (i < (attempts - 1)):
            msg = ''
            if (resp is not None):
                msg = '-> {method} {url} ({code}): {text}'.format(method=resp.request.method, url=resp.url, code=resp.status_code, text=resp.content)
            logger.warning('attempt %s %s', (i + 1), msg)
            time.sleep((i * backoff))
    if (resp is not None):
        if ((resp.status_code == 404) and none_on_404):
            return None
        if (not resp.ok):
            raise GenieHTTPError(resp)
        if (raise_not_status and (resp.status_code != raise_not_status)):
            raise GenieHTTPError(resp)
        return resp
    elif (len(errors) > 0):
        raise errors[(- 1)]
