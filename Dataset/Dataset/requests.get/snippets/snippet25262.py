import json
import re
import os
import time
import http.cookiejar as cookielib
import bs4
import requests
from requests import RequestException
from nautapy import appdata_path
from nautapy.__about__ import __name__ as prog_name
from nautapy.exceptions import NautaLoginException, NautaLogoutException, NautaException, NautaPreLoginException


@classmethod
def is_connected(cls, timeout=3):
    try:
        r = requests.get(CHECK_PAGE, timeout=timeout)
        return (LOGIN_DOMAIN not in r.content)
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False
