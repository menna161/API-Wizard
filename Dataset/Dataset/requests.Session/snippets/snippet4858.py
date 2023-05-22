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


def personal_request(self, method: str, url: str, json: Optional[dict]=None, raise_for_status: bool=True) -> requests.Response:
    '\n        Does a request but using the personal account name and token\n        '
    if (not json):
        json = {}

    def prepare():
        headers = {'Authorization': f'token {self.personal_account_token}', 'Host': 'api.github.com', 'User-Agent': 'python/requests'}
        req = requests.Request(method, url, headers=headers, json=json)
        return req.prepare()
    with requests.Session() as s:
        response = s.send(prepare())
        if (response.status_code == 401):
            self.regen_token()
            response = s.send(prepare())
        if raise_for_status:
            response.raise_for_status()
        return response
