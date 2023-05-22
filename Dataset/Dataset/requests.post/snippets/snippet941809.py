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
def login(email, key):
    '\n            Login to Copyleaks authentication server.\n            For more info: https://api.copyleaks.com/documentation/v3/account/login\n\n            Parameters:\n                email: string. Copyleaks account email address.\n                key: string. Copyleaks account secret key.\n\n            Raises:\n                `CommandError`: Server reject the request. See response status code, headers and content for more info.\n                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff\n\n            Returns:\n                A authentication token that being expired after certain amount of time.\n        '
    assert (email and key)
    url = f'{Consts.IDENTITY_SERVER_URI}/v3/account/login/api'
    payload = {'email': email, 'key': key}
    headers = {'Content-Type': 'application/json', 'User-Agent': Consts.USER_AGENT}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.ok:
        return response.json()
    elif (response.status_code == 503):
        raise UnderMaintenanceError()
    else:
        raise CommandError(response)
