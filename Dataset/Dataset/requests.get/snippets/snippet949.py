from __future__ import print_function
import logging
import requests
from bs4 import BeautifulSoup
from six.moves.urllib import parse as urlparse


def get_feed(self, url):
    try:
        r = requests.get(url, headers={'User-Agent': self.user_agent}, timeout=self.timeout)
    except Exception as e:
        logging.warning("Error while getting '{0}'".format(url))
        logging.warning('{0}'.format(e))
        return None
    return r.text
