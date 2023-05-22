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
def usages_history_csv(auth_token, start_date, end_date):
    '\n            This endpoint allows you to export your usage history between two dates.\n            The output results will be exported to a csv file and it will be attached to the response.\n            For more info: \n            https://api.copyleaks.com/documentation/v3/scans/usages/history\n\n            Parameters: \n                auth_token: Your login token to Copyleaks server.\n                start_date: String. The start date to collect usage history from. Date Format: `dd-MM-yyyy`\n                end_date: String. The end date to collect usage history from. Date Format: `dd-MM-yyyy`\n\n            Raises:\n                `CommandError`: Server reject the request. See response status code, headers and content for more info.\n                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff\n                `RateLimitError`: Too many requests. Please wait before calling again.\n\n            Returns: \n                Server response including success/failed info.\n        '
    assert (start_date and end_date)
    Copyleaks.verify_auth_token(auth_token)
    url = f'{Consts.API_SERVER_URI}/v3/scans/usages/history?start={start_date}&end={end_date}'
    headers = {'Content-Type': 'application/json', 'User-Agent': Consts.USER_AGENT, 'Authorization': f"Bearer {auth_token['access_token']}"}
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.content
    elif (response.status_code == 503):
        raise UnderMaintenanceError()
    elif (response.status_code == 429):
        raise RateLimitError()
    else:
        raise CommandError(response)
