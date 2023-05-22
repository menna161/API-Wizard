import requests
import json


def get_request(path, params=None):
    if (not params):
        params = {}
    r = requests.get(('%s%s' % (api, path)), params=params)
    return r.json()
