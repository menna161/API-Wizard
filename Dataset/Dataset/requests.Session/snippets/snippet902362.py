import base64
import hashlib
import os
import requests
import sys
import warnings
import pytest
from requests.auth import AuthBase
from ntlm_auth.constants import NegotiateFlags
from ntlm_auth.exceptions import NoAuthContextError
from ntlm_auth.gss_channel_bindings import GssChannelBindingsStruct
from ntlm_auth.ntlm import Ntlm, NtlmContext
from ntlm_auth.session_security import SessionSecurity
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
from requests.packages.urllib3.exceptions import SNIMissingWarning
from urllib3.exceptions import InsecureRequestWarning


def _send_request(self, server, domain, username, password, port, ntlm_compatibility, legacy=True):
    '\n        Sends a request to the url with the credentials specified. Returns the\n        final response\n        '
    try:
        from requests.packages.urllib3.exceptions import InsecurePlatformWarning
        warnings.simplefilter('ignore', category=InsecurePlatformWarning)
    except ImportError:
        pass
    try:
        from requests.packages.urllib3.exceptions import SNIMissingWarning
        warnings.simplefilter('ignore', category=SNIMissingWarning)
    except ImportError:
        pass
    try:
        from urllib3.exceptions import InsecureRequestWarning
        warnings.simplefilter('ignore', category=InsecureRequestWarning)
    except ImportError:
        pass
    url = ('%s://%s:%d/contents.txt' % (('http' if str(port).startswith('8') else 'https'), server, port))
    session = requests.Session()
    session.verify = False
    session.auth = NtlmAuth(domain, username, password, ntlm_compatibility, legacy)
    request = requests.Request('GET', url)
    prepared_request = session.prepare_request(request)
    response = session.send(prepared_request)
    return response
