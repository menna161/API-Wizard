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
def start(auth_token, model):
    '\n            Start scanning all the files you submitted for a price-check.\n            For more info: \n            https://api.copyleaks.com/documentation/v3/scans/start\n\n            Parameters: \n                auth_token: Your login token to Copyleaks server.\n                model: `Start` object. Include information about which scans should be started.\n\n            Raises:\n                `CommandError`: Server reject the request. See response status code, headers and content for more info.\n                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff\n\n            Returns: \n                Server response including success/failed info.\n        '
    assert model
    Copyleaks.verify_auth_token(auth_token)
    url = f'{Consts.API_SERVER_URI}/v3/scans/start'
    headers = {'Content-Type': 'application/json', 'User-Agent': Consts.USER_AGENT, 'Authorization': f"Bearer {auth_token['access_token']}"}
    response = requests.patch(url, headers=headers, data=model.toJSON())
    if response.ok:
        return response.json()
    elif (response.status_code == 503):
        raise UnderMaintenanceError()
    else:
        raise CommandError(response)
