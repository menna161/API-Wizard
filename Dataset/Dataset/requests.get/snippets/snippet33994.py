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


def send_ip(self, ipaddr, apikey):
    '\n        Send IP address for list of past malicous domain associations\n        '
    url = (self.base_url + 'ip-address/report')
    parameters = {'ip': ipaddr, 'apikey': apikey}
    rate_limit_clear = self.rate_limit()
    if rate_limit_clear:
        response = requests.get(url, params=parameters)
        if (response.status_code == self.HTTP_OK):
            json_response = response.json()
            return json_response
        elif (response.status_code == self.HTTP_RATE_EXCEEDED):
            time.sleep(20)
        else:
            self.logger.error('sent: %s, HTTP: %d', ipaddr, response.status_code)
        time.sleep(self.public_api_sleep_time)
