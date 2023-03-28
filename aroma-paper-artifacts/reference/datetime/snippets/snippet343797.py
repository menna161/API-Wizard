import hmac
import base64
import requests
import json
import datetime


def _get_timestamp(self):
    timestamp = (datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:(- 3)] + 'Z')
    return timestamp
