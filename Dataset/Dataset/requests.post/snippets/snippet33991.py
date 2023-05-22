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


def scan_file(self, filename, apikey):
    '\n        Sends a file to virus total for assessment\n        '
    url = (self.base_url + 'file/scan')
    params = {'apikey': apikey}
    scanfile = {'file': open(filename, 'rb')}
    response = requests.post(url, files=scanfile, params=params)
    rate_limit_clear = self.rate_limit()
    if rate_limit_clear:
        if (response.status_code == self.HTTP_OK):
            json_response = response.json()
            return json_response
        elif (response.status_code == self.HTTP_RATE_EXCEEDED):
            time.sleep(20)
        else:
            self.logger.error('sent: %s, HTTP: %d', filename, response.status_code)
