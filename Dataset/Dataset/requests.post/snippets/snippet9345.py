import urllib
from typing import List, Optional
from json import JSONDecodeError
import requests
from .exceptions import PCORequestException
from .exceptions import PCORequestTimeoutException
from .exceptions import PCOUnexpectedRequestException


def get_cc_org_token(cc_name: Optional[str]=None) -> Optional[str]:
    'Get a non-authenticated Church Center OrganizationToken.\n\n    Args:\n        cc_name (str): The organization_name part of the organization_name.churchcenter.com url.\n\n    Raises:\n\n    Returns:\n        str: String of organization token\n    '
    try:
        response = requests.post(f'https://{cc_name}.churchcenter.com/sessions/tokens', timeout=30)
    except requests.exceptions.Timeout as err:
        raise PCORequestTimeoutException() from err
    except Exception as err:
        raise PCOUnexpectedRequestException(str(err)) from err
    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        raise PCORequestException(response.status_code, str(err), response_body=response.text) from err
    try:
        response.json()
        return str(response.json()['data']['attributes']['token'])
    except JSONDecodeError as err:
        raise PCOUnexpectedRequestException('Invalid Church Center URL') from err
