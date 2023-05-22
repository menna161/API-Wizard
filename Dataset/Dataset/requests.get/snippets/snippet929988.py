from typing import Dict, Iterator
import requests
from lxml import etree


def get_url(url: str) -> str:
    'extract special url'
    try:
        r = requests.get(url, allow_redirects=False, timeout=15)
        if ((r.status_code == 302) and ('Location' in r.headers.keys())):
            return r.headers['Location']
    except Exception:
        pass
    return ''
