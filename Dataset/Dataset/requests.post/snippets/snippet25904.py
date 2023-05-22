import requests
import logging
from trustpilot import auth, utils
from os import environ
from warnings import warn
import requests.packages.urllib3


def get_request_auth_headers(self):
    (url, data, headers) = auth.create_access_token_request_params(self)
    response = requests.post(url=url, headers=headers, data=data)
    self.access_token = None
    if (response and (response.status_code == requests.codes['ok'])):
        response_json = response.json()
        self.access_token = response_json['access_token']
    self.headers.update({'Authorization': 'Bearer {}'.format(self.access_token), 'apikey': self.api_key, 'User-Agent': self.user_agent})
    return self.headers
