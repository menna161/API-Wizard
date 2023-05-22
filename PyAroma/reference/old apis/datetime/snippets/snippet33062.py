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


def _datetime_to_secs(utc_time):
    epoch = datetime.datetime(1970, 1, 1)
    time_delta = (utc_time - epoch)
    return ((time_delta.days * 86400) + time_delta.seconds)
