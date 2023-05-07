from bs4 import BeautifulSoup
from six.moves.urllib.parse import urlsplit, urlunsplit
import warnings
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
import copy
from .. import lib


def raise_if_form_exists(url, session):
    '\n    This function raises a UserWarning if the link has forms\n    '
    user_warning = ('Navigate to {0}, '.format(url) + 'login and follow instructions. It is likely that you have to perform some one-time registration steps before acessing this data.')
    resp = session.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')
    if (len(soup.select('form')) > 0):
        raise UserWarning(user_warning)
