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
def get_user_credit(cls, session, username, password):
    r = session.requests_session.post('https://secure.etecsa.net:8443/EtecsaQueryServlet', {'CSRFHW': session.csrfhw, 'wlanuserip': session.wlanuserip, 'username': username, 'password': password})
    if (not r.ok):
        raise NautaException('Fallo al obtener la información del usuario: {} - {}'.format(r.status_code, r.reason))
    if ('secure.etecsa.net' not in r.url):
        raise NautaException('No se puede obtener el crédito del usuario mientras está online')
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    credit_tag = soup.select_one('#sessioninfo > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)')
    if (not credit_tag):
        raise NautaException('Fallo al obtener el crédito del usuario: no se encontró la información')
    return credit_tag.get_text().strip()
