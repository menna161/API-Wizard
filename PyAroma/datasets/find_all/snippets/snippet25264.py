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
def login(cls, session, username, password):
    r = session.requests_session.post(session.login_action, {'CSRFHW': session.csrfhw, 'wlanuserip': session.wlanuserip, 'username': username, 'password': password})
    if (not r.ok):
        raise NautaLoginException('Falló el inicio de sesión: {} - {}'.format(r.status_code, r.reason))
    if (not ('online.do' in r.url)):
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        script_text = soup.find_all('script')[(- 1)].get_text()
        match = re.search('alert\\(\\"(?P<reason>[^\\"]*?)\\"\\)', script_text)
        raise NautaLoginException('Falló el inicio de sesión: {}'.format((match and match.groupdict().get('reason'))))
    m = re.search('ATTRIBUTE_UUID=(\\w+)&CSRFHW=', r.text)
    return (m.group(1) if m else None)
