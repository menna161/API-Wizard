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
def resend_webhook(auth_token, scan_id):
    '\n            Resend status webhooks for existing scans.\n            For more info: \n            https://api.copyleaks.com/documentation/v3/scans/webhook-resend\n\n            Raises:\n                `CommandError`: Server reject the request. See response status code, headers and content for more info.\n                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff\n        '
    assert scan_id
    Copyleaks.verify_auth_token(auth_token)
    url = f'{Consts.API_SERVER_URI}/v3/scans/{scan_id}/webhooks/resend'
    headers = {'Content-Type': 'application/json', 'User-Agent': Consts.USER_AGENT, 'Authorization': f"Bearer {auth_token['access_token']}"}
    response = requests.post(url, headers=headers)
    if response.ok:
        return
    elif (response.status_code == 503):
        raise UnderMaintenanceError()
    else:
        raise CommandError(response)
