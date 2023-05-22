import json
import hmac
import base64
import requests
import datetime
import urllib.parse
from enum import Enum


def __toISO8601(self, time):
    return (time.replace(tzinfo=datetime.timezone.utc).isoformat().split('+')[0] + 'Z')
