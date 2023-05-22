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
def supported_file_types():
    '\n            Get a list of the supported file types.\n            For more info: https://api.copyleaks.com/documentation/v3/specifications/supported-file-types\n\n            Raises:\n                `CommandError`: Server reject the request. See response status code, headers and content for more info.\n                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff\n\n            Returns:\n                List of supported file types.\n        '
    url = f'{Consts.API_SERVER_URI}/v3/miscellaneous/supported-file-types'
    headers = {'User-Agent': Consts.USER_AGENT}
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    elif (response.status_code == 503):
        raise UnderMaintenanceError()
    else:
        raise CommandError(response)
