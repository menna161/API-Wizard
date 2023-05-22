from __future__ import unicode_literals
import json
import sys
from copy import deepcopy
import requests
from requests.exceptions import HTTPError


def __init__(self, provided_settings, prefix, category):
    '\n        Object instantiation.\n\n        User settings get set and verified, _category and _prefix attributes are set.\n\n        Parameters\n        ----------\n        provided_settings: str\n            Original settings dict supplied by the user from the rtpy.Rtpy class\n        prefix: str\n            API endpoint used for a given API method category ("search/"...)\n        category: str\n            Major API method category (Searches, Repositories...)\n\n        '
    self._category = category
    self._prefix = prefix
    self._user_settings = {'af_url': None, 'api_key': None, 'username': None, 'password': None, 'raw_response': False, 'verbose_level': 0, 'auth': (), 'X-JFrog-Art-Api': None, 'api_endpoint': None, 'session': requests.Session()}
    self._configure_user_settings(provided_settings)
    self._validate_user_settings()
