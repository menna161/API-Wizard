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


def __init__(self, access_token, client_id, client_secret, refresh_token, token_expiry, token_uri, user_agent, revoke_uri=GOOGLE_REVOKE_URI):
    "Create an instance of GoogleCredentials.\n\n        This constructor is not usually called by the user, instead\n        GoogleCredentials objects are instantiated by\n        GoogleCredentials.from_stream() or\n        GoogleCredentials.get_application_default().\n\n        Args:\n            access_token: string, access token.\n            client_id: string, client identifier.\n            client_secret: string, client secret.\n            refresh_token: string, refresh token.\n            token_expiry: datetime, when the access_token expires.\n            token_uri: string, URI of token endpoint.\n            user_agent: string, The HTTP User-Agent to provide for this\n                        application.\n            revoke_uri: string, URI for revoke endpoint. Defaults to\n                        GOOGLE_REVOKE_URI; a token can't be revoked if this\n                        is None.\n        "
    super(GoogleCredentials, self).__init__(access_token, client_id, client_secret, refresh_token, token_expiry, token_uri, user_agent, revoke_uri=revoke_uri)
