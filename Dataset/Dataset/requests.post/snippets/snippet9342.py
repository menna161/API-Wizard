import urllib
from typing import List, Optional
from json import JSONDecodeError
import requests
from .exceptions import PCORequestException
from .exceptions import PCORequestTimeoutException
from .exceptions import PCOUnexpectedRequestException


def _do_oauth_post(url: str, **kwargs) -> requests.Response:
    'Do a Post request to facilitate the OAUTH process.\n\n    Handles error handling appropriately and raises pypco exceptions.\n\n    Args:\n        url (str): The url to which the request should be made.\n        **kwargs: Data fields sent as the request payload.\n\n    Raises:\n        PCORequestTimeoutException: The request timed out.\n        PCOUnexpectedRequestException: Something unexpected went wrong with the request.\n        PCORequestException: The HTTP response from PCO indicated an error.\n\n    Returns:\n        requests.Response: The response object from the request.\n    '
    try:
        response = requests.post(url, data={**kwargs}, headers={'User-Agent': 'pypco'}, timeout=30)
    except requests.exceptions.Timeout as err:
        raise PCORequestTimeoutException() from err
    except Exception as err:
        raise PCOUnexpectedRequestException(str(err)) from err
    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        raise PCORequestException(response.status_code, str(err), response_body=response.text) from err
    return response
