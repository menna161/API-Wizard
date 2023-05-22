import requests
import logging
from . import ppp
import pyroute2
import ipaddress
import atexit
import subprocess
import sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


def run(self):
    self.host = (self.options.server + (':%d' % self.options.port))
    self.session = requests.Session()
    if self.options.fingerprint:
        self.session.verify = False
        self.session.mount('https://', FingerprintAdapter(self.options.fingerprint))
    self.session.headers = {'User-Agent': 'Dell SonicWALL NetExtender for Linux 8.1.789'}
    logging.info('Logging in...')
    self.login(self.options.username, self.options.password, self.options.domain)
    logging.info('Starting session...')
    self.start_session()
    logging.info('Dialing up tunnel...')
    self.tunnel()
