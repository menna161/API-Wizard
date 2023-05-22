import logging
import os.path
import requests
from requests.packages.urllib3.exceptions import SubjectAltNameWarning


def __get_session(self, auth):
    session = requests.Session()
    session.trust_env = False
    requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)
    if self.certfile:
        session.verify = self.certfile
    session.auth = auth
    opsicon_logger.debug(('Created new session: %s}' % session))
    return session
