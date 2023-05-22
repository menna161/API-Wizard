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
def create_session(cls):
    if cls.is_connected():
        if SessionObject.is_logged_in():
            raise NautaPreLoginException('Hay una sessión abierta')
        else:
            raise NautaPreLoginException('Hay una conexión activa')
    session = SessionObject()
    resp = session.requests_session.get(LOGIN_URL)
    if (not resp.ok):
        raise NautaPreLoginException('Failed to create session')
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    action = LOGIN_URL
    data = cls._get_inputs(soup)
    resp = session.requests_session.post(action, data)
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    form_soup = soup.find('form', id='formulario')
    session.login_action = form_soup['action']
    data = cls._get_inputs(form_soup)
    session.csrfhw = data['CSRFHW']
    session.wlanuserip = data['wlanuserip']
    return session
