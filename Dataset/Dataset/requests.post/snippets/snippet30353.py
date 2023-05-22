from dexy.filters.api import ApiFilter
import requests
import json
from dexy.exceptions import UserFeedback


def oauth_post_request(self, params):
    url = (self.read_param('site') + '/oauth/token/')
    r = requests.post(url, data=params, verify=self.setting('verify-ssl'))
    token_info = r.json()
    self.write_params(token_info)
