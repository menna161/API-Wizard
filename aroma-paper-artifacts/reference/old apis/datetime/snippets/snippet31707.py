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


@util.positional(8)
def __init__(self, access_token, client_id, client_secret, refresh_token, token_expiry, token_uri, user_agent, revoke_uri=None, id_token=None, token_response=None, scopes=None, token_info_uri=None):
    "Create an instance of OAuth2Credentials.\n\n        This constructor is not usually called by the user, instead\n        OAuth2Credentials objects are instantiated by the OAuth2WebServerFlow.\n\n        Args:\n            access_token: string, access token.\n            client_id: string, client identifier.\n            client_secret: string, client secret.\n            refresh_token: string, refresh token.\n            token_expiry: datetime, when the access_token expires.\n            token_uri: string, URI of token endpoint.\n            user_agent: string, The HTTP User-Agent to provide for this\n                        application.\n            revoke_uri: string, URI for revoke endpoint. Defaults to None; a\n                        token can't be revoked if this is None.\n            id_token: object, The identity of the resource owner.\n            token_response: dict, the decoded response to the token request.\n                            None if a token hasn't been requested yet. Stored\n                            because some providers (e.g. wordpress.com) include\n                            extra fields that clients may want.\n            scopes: list, authorized scopes for these credentials.\n          token_info_uri: string, the URI for the token info endpoint. Defaults\n                          to None; scopes can not be refreshed if this is None.\n\n        Notes:\n            store: callable, A callable that when passed a Credential\n                   will store the credential back to where it came from.\n                   This is needed to store the latest access_token if it\n                   has expired and been refreshed.\n        "
    self.access_token = access_token
    self.client_id = client_id
    self.client_secret = client_secret
    self.refresh_token = refresh_token
    self.store = None
    self.token_expiry = token_expiry
    self.token_uri = token_uri
    self.user_agent = user_agent
    self.revoke_uri = revoke_uri
    self.id_token = id_token
    self.token_response = token_response
    self.scopes = set(util.string_to_scopes((scopes or [])))
    self.token_info_uri = token_info_uri
    self.invalid = False
