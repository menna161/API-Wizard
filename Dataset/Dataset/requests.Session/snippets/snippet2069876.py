from __future__ import print_function
import logging
import sys
import requests
from icinga2api.exceptions import Icinga2ApiException
from urllib.parse import urljoin
from urlparse import urljoin


def _create_session(self, method='POST'):
    '\n        create a session object\n        '
    session = requests.Session()
    if (self.manager.certificate and self.manager.key):
        session.cert = (self.manager.certificate, self.manager.key)
    elif self.manager.certificate:
        session.cert = self.manager.certificate
    elif (self.manager.username and self.manager.password):
        session.auth = (self.manager.username, self.manager.password)
    session.headers = {'User-Agent': 'Python-icinga2api/{0}'.format(self.manager.version), 'X-HTTP-Method-Override': method.upper(), 'Accept': 'application/json'}
    return session
