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


@classmethod
def from_json(cls, json_data):
    'Deserialize a JSON-serialized instance.\n\n        Inverse to :meth:`to_json`.\n\n        Args:\n            json_data: dict or string, Serialized JSON (as a string or an\n                       already parsed dictionary) representing a credential.\n\n        Returns:\n            ServiceAccountCredentials from the serialized data.\n        '
    if (not isinstance(json_data, dict)):
        json_data = json.loads(_from_bytes(json_data))
    private_key_pkcs8_pem = None
    pkcs12_val = json_data.get(_PKCS12_KEY)
    password = None
    if (pkcs12_val is None):
        private_key_pkcs8_pem = json_data['_private_key_pkcs8_pem']
        signer = crypt.Signer.from_string(private_key_pkcs8_pem)
    else:
        pkcs12_val = base64.b64decode(pkcs12_val)
        password = json_data['_private_key_password']
        signer = crypt.Signer.from_string(pkcs12_val, password)
    credentials = cls(json_data['_service_account_email'], signer, scopes=json_data['_scopes'], private_key_id=json_data['_private_key_id'], client_id=json_data['client_id'], user_agent=json_data['_user_agent'], **json_data['_kwargs'])
    if (private_key_pkcs8_pem is not None):
        credentials._private_key_pkcs8_pem = private_key_pkcs8_pem
    if (pkcs12_val is not None):
        credentials._private_key_pkcs12 = pkcs12_val
    if (password is not None):
        credentials._private_key_password = password
    credentials.invalid = json_data['invalid']
    credentials.access_token = json_data['access_token']
    credentials.token_uri = json_data['token_uri']
    credentials.revoke_uri = json_data['revoke_uri']
    token_expiry = json_data.get('token_expiry', None)
    if (token_expiry is not None):
        credentials.token_expiry = datetime.datetime.strptime(token_expiry, EXPIRY_FORMAT)
    return credentials
