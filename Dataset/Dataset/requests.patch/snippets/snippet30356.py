from dexy.filters.api import ApiFilter
import requests
import json
from dexy.exceptions import UserFeedback


def api_request(self, verb, url, json=None):
    if (verb == 'get'):
        return requests.get(url, params={'_format': 'json'}, headers=self.gen_headers(), verify=self.setting('verify-ssl'))
    elif (verb == 'post'):
        return requests.post(url, params={'_format': 'json'}, headers=self.gen_headers(), verify=self.setting('verify-ssl'), json=json)
    elif (verb == 'patch'):
        return requests.patch(url, params={'_format': 'json'}, headers=self.gen_headers(), verify=self.setting('verify-ssl'), json=json)
    else:
        raise Exception(("unknown rest verb '%s'" % verb))
