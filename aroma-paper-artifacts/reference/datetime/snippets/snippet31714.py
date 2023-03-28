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
def from_json(cls, json_data):
    'Instantiate a Credentials object from a JSON description of it.\n\n        The JSON should have been produced by calling .to_json() on the object.\n\n        Args:\n            json_data: string or bytes, JSON to deserialize.\n\n        Returns:\n            An instance of a Credentials subclass.\n        '
    data = json.loads(_from_bytes(json_data))
    if (data.get('token_expiry') and (not isinstance(data['token_expiry'], datetime.datetime))):
        try:
            data['token_expiry'] = datetime.datetime.strptime(data['token_expiry'], EXPIRY_FORMAT)
        except ValueError:
            data['token_expiry'] = None
    retval = cls(data['access_token'], data['client_id'], data['client_secret'], data['refresh_token'], data['token_expiry'], data['token_uri'], data['user_agent'], revoke_uri=data.get('revoke_uri', None), id_token=data.get('id_token', None), token_response=data.get('token_response', None), scopes=data.get('scopes', None), token_info_uri=data.get('token_info_uri', None))
    retval.invalid = data['invalid']
    return retval
