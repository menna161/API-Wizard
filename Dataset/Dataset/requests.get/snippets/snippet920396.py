import logging
import json
import os
import random
import string
import sys
import pprint
import threading
import tempfile
import modules.urllib3 as urllib3
from urllib.parse import parse_qs
from typing import Dict, List
from http.server import HTTPServer, BaseHTTPRequestHandler
from enum import Enum
import modules.requests as requests


def __api_get_account_info(self, character_id: str):
    resp = requests.get(((self.API_DOMAIN + self.API_URL_CHARACTER) + character_id), params={'data': 'AC,FR'})
    result = None
    try:
        result = json.loads(resp.text)
    except Exception:
        logging.error(('ffxivapi/__api_get_account_info: %s' % resp.text))
    return (resp.status_code, result)
