import requests
from django.http.response import JsonResponse
import logging
from requests import HTTPError


@staticmethod
def _send_request(method, url, **kwargs):
    'Send request by method and url.\n         Raises HTTPError exceptions if status >= 400\n\n         Returns:\n             json: Response body\n         '
    response = requests.request(method, url, **kwargs)
    response.raise_for_status()
    return response.json()
