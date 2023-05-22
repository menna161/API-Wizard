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
def __submit(url, auth_token, scan_id, submission):
    assert (url and scan_id and submission)
    Copyleaks.verify_auth_token(auth_token)
    headers = {'Content-Type': 'application/json', 'User-Agent': Consts.USER_AGENT, 'Authorization': f"Bearer {auth_token['access_token']}"}
    response = requests.put(url, headers=headers, data=submission.toJSON())
    if response.ok:
        return
    elif (response.status_code == 503):
        raise UnderMaintenanceError()
    else:
        raise CommandError(response)
