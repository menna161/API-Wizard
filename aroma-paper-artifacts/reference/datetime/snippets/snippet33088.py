import base64
import copy
import datetime
import httplib2
import json
import time
from oauth2client import GOOGLE_REVOKE_URI
from oauth2client import GOOGLE_TOKEN_URI
from oauth2client._helpers import _json_encode
from oauth2client._helpers import _from_bytes
from oauth2client._helpers import _urlsafe_b64encode
from oauth2client import util
from oauth2client.client import _apply_user_agent
from oauth2client.client import _initialize_headers
from oauth2client.client import AccessTokenInfo
from oauth2client.client import AssertionCredentials
from oauth2client.client import clean_headers
from oauth2client.client import EXPIRY_FORMAT
from oauth2client.client import GoogleCredentials
from oauth2client.client import SERVICE_ACCOUNT
from oauth2client.client import TokenRevokeError
from oauth2client.client import _UTCNOW
from oauth2client import crypt


def _create_token(self, additional_claims=None):
    now = _UTCNOW()
    expiry = (now + datetime.timedelta(seconds=self._MAX_TOKEN_LIFETIME_SECS))
    payload = {'iat': _datetime_to_secs(now), 'exp': _datetime_to_secs(expiry), 'iss': self._service_account_email, 'sub': self._service_account_email}
    payload.update(self._kwargs)
    if (additional_claims is not None):
        payload.update(additional_claims)
    jwt = crypt.make_signed_jwt(self._signer, payload, key_id=self._private_key_id)
    return (jwt.decode('ascii'), expiry)
