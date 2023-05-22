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
def export(auth_token, scan_id, export_id, model):
    '\n            Exporting scans artifact into your server. \n            For more info: \n            https://api.copyleaks.com/documentation/v3/downloads/export\n\n            Parameters: \n                auth_token: Your login token to Copyleaks server.\n                scan_id: String. The scan ID of the specific scan to export.\n                export_id: String. A new Id for the export process.\n                model: `Export`. Request of which artifact should be exported.\n\n            Raises:\n                `CommandError`: Server reject the request. See response status code, headers and content for more info.\n                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff\n        '
    assert (scan_id and export_id and model)
    Copyleaks.verify_auth_token(auth_token)
    url = f'{Consts.API_SERVER_URI}/v3/downloads/{scan_id}/export/{export_id}'
    headers = {'Content-Type': 'application/json', 'User-Agent': Consts.USER_AGENT, 'Authorization': f"Bearer {auth_token['access_token']}"}
    response = requests.post(url, headers=headers, data=model.toJSON())
    if response.ok:
        return
    elif (response.status_code == 503):
        raise UnderMaintenanceError()
    else:
        raise CommandError(response)
