import base64
import collections
import copy
import datetime
import json
import logging
import os
import socket
import sys
import tempfile
import time
import shutil
import six
from six.moves import http_client
from six.moves import urllib
import httplib2
from oauth2client import GOOGLE_AUTH_URI
from oauth2client import GOOGLE_DEVICE_URI
from oauth2client import GOOGLE_REVOKE_URI
from oauth2client import GOOGLE_TOKEN_URI
from oauth2client import GOOGLE_TOKEN_INFO_URI
from oauth2client._helpers import _from_bytes
from oauth2client._helpers import _to_bytes
from oauth2client._helpers import _urlsafe_b64decode
from oauth2client import clientsecrets
from oauth2client import util
from oauth2client import crypt
from oauth2client.contrib.appengine import AppAssertionCredentials
from oauth2client.contrib.gce import AppAssertionCredentials
import google.appengine
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.service_account import _JWTAccessCredentials
from oauth2client.service_account import _JWTAccessCredentials


def _do_refresh_request(self, http_request):
    'Refresh the access_token using the refresh_token.\n\n        Args:\n            http_request: callable, a callable that matches the method\n                          signature of httplib2.Http.request, used to make the\n                          refresh request.\n\n        Raises:\n            HttpAccessTokenRefreshError: When the refresh fails.\n        '
    body = self._generate_refresh_request_body()
    headers = self._generate_refresh_request_headers()
    logger.info('Refreshing access_token')
    (resp, content) = http_request(self.token_uri, method='POST', body=body, headers=headers)
    content = _from_bytes(content)
    if (resp.status == http_client.OK):
        d = json.loads(content)
        self.token_response = d
        self.access_token = d['access_token']
        self.refresh_token = d.get('refresh_token', self.refresh_token)
        if ('expires_in' in d):
            delta = datetime.timedelta(seconds=int(d['expires_in']))
            self.token_expiry = (delta + _UTCNOW())
        else:
            self.token_expiry = None
        if ('id_token' in d):
            self.id_token = _extract_id_token(d['id_token'])
        else:
            self.id_token = None
        self.invalid = False
        if self.store:
            self.store.locked_put(self)
    else:
        logger.info('Failed to retrieve access token: %s', content)
        error_msg = ('Invalid response %s.' % (resp['status'],))
        try:
            d = json.loads(content)
            if ('error' in d):
                error_msg = d['error']
                if ('error_description' in d):
                    error_msg += (': ' + d['error_description'])
                self.invalid = True
                if (self.store is not None):
                    self.store.locked_put(self)
        except (TypeError, ValueError):
            pass
        raise HttpAccessTokenRefreshError(error_msg, status=resp.status)
