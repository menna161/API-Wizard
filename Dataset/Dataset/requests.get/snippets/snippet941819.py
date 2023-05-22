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
def credits_balance(auth_token):
    '\n            Get current credits balance for the Copyleaks account\n            For more info: \n            https://api.copyleaks.com/documentation/v3/scans/credits\n\n            Raises:\n                `CommandError`: Server reject the request. See response status code, headers and content for more info.\n                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff\n                `RateLimitError`: Too many requests. Please wait before calling again.\n\n            Returns:\n                Number of remaining credits on the account.\n        '
    Copyleaks.verify_auth_token(auth_token)
    url = f'{Consts.API_SERVER_URI}/v3/scans/credits'
    headers = {'User-Agent': Consts.USER_AGENT, 'Authorization': f"Bearer {auth_token['access_token']}"}
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    elif (response.status_code == 503):
        raise UnderMaintenanceError()
    elif (response.status_code == 429):
        raise RateLimitError()
    else:
        raise CommandError(response)
