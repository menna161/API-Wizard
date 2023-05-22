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


def rescan_file(self, filename, sha256hash, apikey):
    '\n        just send the hash, check the date\n        '
    url = (self.base_url + 'file/rescan')
    params = {'apikey': apikey, 'resource': sha256hash}
    rate_limit_clear = self.rate_limit()
    if rate_limit_clear:
        response = requests.post(url, params=params)
        if (response.status_code == self.HTTP_OK):
            self.logger.info('sent: %s, HTTP: %d, content: %s', os.path.basename(filename), response.status_code, response.text)
        elif (response.status_code == self.HTTP_RATE_EXCEEDED):
            time.sleep(20)
        else:
            self.logger.error('sent: %s, HTTP: %d', os.path.basename(filename), response.status_code)
        return response
