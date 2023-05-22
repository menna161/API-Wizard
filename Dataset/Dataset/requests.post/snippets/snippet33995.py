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


def url_report(self, scan_url, apikey):
    '\n        Send URLS for list of past malicous associations\n        '
    url = (self.base_url + 'url/report')
    params = {'apikey': apikey, 'resource': scan_url}
    rate_limit_clear = self.rate_limit()
    if rate_limit_clear:
        response = requests.post(url, params=params, headers=self.headers)
        if (response.status_code == self.HTTP_OK):
            json_response = response.json()
            return json_response
        elif (response.status_code == self.HTTP_RATE_EXCEEDED):
            time.sleep(20)
        else:
            self.logger.error('sent: %s, HTTP: %d', scan_url, response.status_code)
        time.sleep(self.public_api_sleep_time)
