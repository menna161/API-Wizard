from bs4 import BeautifulSoup
from six.moves.urllib.parse import urlsplit, urlunsplit
import warnings
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
import copy
from .. import lib


def soup_login(session, url, username, password, username_field='username', password_field='password'):
    resp = session.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')
    login_form = soup.select('form')[0]

    def get_to_url(current_url, to_url):
        split_current = urlsplit(current_url)
        split_to = urlsplit(to_url)
        comb = [(val2 if (val1 == '') else val1) for (val1, val2) in zip(split_to, split_current)]
        return urlunsplit(comb)
    to_url = get_to_url(resp.url, login_form.get('action'))
    session.headers['Referer'] = resp.url
    payload = {}
    if (username_field is not None):
        if (len(login_form.findAll('input', {'name': username_field})) > 0):
            payload.update({username_field: username})
    if (password_field is not None):
        if (len(login_form.findAll('input', {'name': password_field})) > 0):
            payload.update({password_field: password})
        else:
            raise Exception('Navigate to {0}. If you are unable to login, you must either wait or use authentication from another service.'.format(url))
    for input in login_form.findAll('input'):
        if ((input.get('name') not in payload) and (input.get('name') is not None)):
            payload.update({input.get('name'): input.get('value')})
    submit_type = 'submit'
    submit_names = [input.get('name') for input in login_form.findAll('input', {'type': submit_type})]
    for input in login_form.findAll('input', {'type': submit_type}):
        if (('submit' in submit_names) and (input.get('name').lower() != 'submit')):
            payload.pop(input.get('name'), None)
    return session.post(to_url, data=payload)
