import json
import logging
import os
import re
import requests
import redis
import sys
import time
import urllib
import uuid
from pylimit import PyRateLimit
import six.moves.configparser


def binary_report(self, sha256sum, apikey):
    '\n        retrieve report from file scan\n        '
    url = (self.base_url + 'file/report')
    params = {'apikey': apikey, 'resource': sha256sum}
    rate_limit_clear = self.rate_limit()
    if rate_limit_clear:
        response = requests.post(url, data=params)
        if (response.status_code == self.HTTP_OK):
            json_response = response.json()
            response_code = json_response['response_code']
            return json_response
        elif (response.status_code == self.HTTP_RATE_EXCEEDED):
            time.sleep(20)
        else:
            self.logger.warning('retrieve report: %s, HTTP code: %d', os.path.basename(filename), response.status_code)
