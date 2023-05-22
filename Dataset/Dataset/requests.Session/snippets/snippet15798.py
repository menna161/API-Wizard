import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from btp.util import req


def __get_session(url):
    session = requests.Session()
    session.mount(url, HTTP_ADAPTER)
    return session
