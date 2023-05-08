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


@classmethod
def FromResponse(cls, response):
    'Create a DeviceFlowInfo from a server response.\n\n        The response should be a dict containing entries as described here:\n\n        http://tools.ietf.org/html/draft-ietf-oauth-v2-05#section-3.7.1\n        '
    kwargs = {'device_code': response['device_code'], 'user_code': response['user_code']}
    verification_url = response.get('verification_url', response.get('verification_uri'))
    if (verification_url is None):
        raise OAuth2DeviceCodeError('No verification_url provided in server response')
    kwargs['verification_url'] = verification_url
    kwargs.update({'interval': response.get('interval'), 'user_code_expiry': None})
    if ('expires_in' in response):
        kwargs['user_code_expiry'] = (_UTCNOW() + datetime.timedelta(seconds=int(response['expires_in'])))
    return cls(**kwargs)
