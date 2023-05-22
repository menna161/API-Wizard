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


def ghrequest(self, method: str, url: str, json: Optional[dict]=None, *, override_accept_header: Optional[str]=None, raise_for_status: Optional[bool]=True) -> requests.Response:
    accept = ACCEPT_HEADER
    if override_accept_header:
        accept = override_accept_header

    def prepare():
        atk = self.token()
        headers = {'Authorization': f'Bearer {atk}', 'Accept': accept, 'Host': 'api.github.com', 'User-Agent': 'python/requests'}
        print(f'Making a {method} call to {url}')
        req = requests.Request(method, url, headers=headers, json=json)
        return req.prepare()
    with requests.Session() as s:
        response = s.send(prepare())
        if (response.status_code == 401):
            self.regen_token()
            response = s.send(prepare())
        if raise_for_status:
            response.raise_for_status()
        rate_limit = response.headers.get('X-RateLimit-Limit', (- 1))
        rate_remaining = response.headers.get('X-RateLimit-Limit', (- 1))
        if rate_limit:
            repo_name_list = [k for (k, v) in self.idmap.items() if (v == self.installation_id)]
            repo_name = 'no-repo'
            if (len(repo_name_list) == 1):
                repo_name = repo_name_list[0]
            elif (len(repo_name_list) == 0):
                repo_name = 'no-matches'
            else:
                repo_name = 'multiple-matches'
            add_event('gh-rate', {'limit': int(rate_limit), 'rate_remaining': int(rate_remaining), 'installation': repo_name})
        return response
