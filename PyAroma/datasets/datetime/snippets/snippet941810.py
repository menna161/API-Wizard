from copyleaks.consts import Consts
import requests
import json
from datetime import datetime, timedelta
import dateutil.parser
import pytz
from copyleaks.exceptions.command_error import CommandError
from copyleaks.exceptions.under_maintenance_error import UnderMaintenanceError
from copyleaks.exceptions.rate_limit_error import RateLimitError
from copyleaks.exceptions.auth_expired_error import AuthExipredError
from enum import Enum


@staticmethod
def verify_auth_token(auth_token):
    '\n            Verify that Copyleaks authentication token is exists and not expired.\n\n            Parameters:\n                auth_token: Copyleaks authentication token\n\n            Raises:\n                `AuthExipredError`: authentication expired. Need to login again.\n        '
    assert (auth_token and auth_token['.expires'] and auth_token['access_token'])
    now = pytz.UTC.localize((datetime.utcnow() + timedelta(0, (5 * 60))))
    upTo = dateutil.parser.parse(auth_token['.expires'])
    if (upTo <= now):
        raise AuthExipredError()
