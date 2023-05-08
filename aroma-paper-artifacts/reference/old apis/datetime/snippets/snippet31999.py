import datetime
import json
import os
import socket
from oauth2client._helpers import _to_bytes
from oauth2client import client


def _refresh(self, http_request):
    self.devshell_response = _SendRecv()
    self.access_token = self.devshell_response.access_token
    expires_in = self.devshell_response.expires_in
    if (expires_in is not None):
        delta = datetime.timedelta(seconds=expires_in)
        self.token_expiry = (_UTCNOW() + delta)
    else:
        self.token_expiry = None
