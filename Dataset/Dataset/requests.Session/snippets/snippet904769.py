from __future__ import print_function
import requests


def __init__(self, token):
    'ZenHub API wrapper.'
    self._token = token
    self._endpoint = 'https://api.zenhub.com/p1/'
    self._session = requests.Session()
    self._session.headers.update(self._HEADERS)
    self._session.headers.update({'X-Authentication-Token': token})
