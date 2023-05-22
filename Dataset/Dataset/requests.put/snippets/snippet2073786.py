import logging
from typing import Any, Dict, Optional
import requests
from . import connection, exceptions, helper


def _rest_request(self, target: str, method: str='GET') -> Dict[(str, Any)]:
    url = self._format_rest_url(target)
    try:
        if (method == 'POST'):
            response = requests.post(url, timeout=self.timeout, verify=False)
        elif (method == 'PUT'):
            response = requests.put(url, timeout=self.timeout, verify=False)
        elif (method == 'DELETE'):
            response = requests.delete(url, timeout=self.timeout, verify=False)
        else:
            response = requests.get(url, timeout=self.timeout, verify=False)
        return helper.process_api_response(response.text)
    except requests.ConnectionError as err:
        raise exceptions.HttpApiError('TV unreachable or feature not supported on this model.') from err
