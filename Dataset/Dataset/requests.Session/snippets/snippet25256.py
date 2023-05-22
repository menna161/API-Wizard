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
def _create_requests_session(cls):
    requests_session = requests.Session()
    requests_session.cookies = cookielib.MozillaCookieJar(NAUTA_SESSION_FILE)
    return requests_session
