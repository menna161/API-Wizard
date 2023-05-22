import requests
import time
import datetime
import typing
import os
from typing import Union, Optional, List, Dict


def _query_cryptocompare(url: str, errorCheck: bool=True, api_key: str=None) -> Optional[Dict]:
    '\n    Query the url and return the result or None on failure.\n\n    :param url: the url\n    :param errorCheck: run extra error checks (default: True)\n    :api_key: optional, if you want to add an API Key\n    :returns: respones, or nothing if errorCheck=True\n    '
    api_key_parameter = _set_api_key_parameter(api_key)
    try:
        response = requests.get((url + api_key_parameter)).json()
    except Exception as e:
        print(f'Error getting coin information. {e}')
        return None
    if (errorCheck and (response.get('Response') == 'Error')):
        msg = response.get('Message')
        print(f'[ERROR] {msg}')
        return None
    return response
