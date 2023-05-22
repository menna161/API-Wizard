import datetime
import json
import pipes
import re
import shlex
import subprocess
from typing import Any, Dict, Optional, cast
import jwt
import requests
from .scopes import Permission
import keen


def _integration_authenticated_request(self, method, url, json=None):
    self.since = int(datetime.datetime.now().timestamp())
    payload = dict({'iat': self.since, 'exp': (self.since + self.duration), 'iss': self.integration_id})
    assert (self.rsadata is not None)
    tok = jwt.encode(payload, key=self.rsadata, algorithm='RS256')
    headers = {'Authorization': f'Bearer {tok}', 'Accept': ACCEPT_HEADER_V3, 'Host': 'api.github.com', 'User-Agent': 'python/requests'}
    req = requests.Request(method, url, headers=headers, json=json)
    prepared = req.prepare()
    with requests.Session() as s:
        return s.send(prepared)
