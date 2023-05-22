import json
import time
from enum import Enum
import requests


def _request(self, payload, endpoint, request_method, files=None, headers=None):
    '\n        Makes a POST request.\n        :param payload: the payload containing the parameters\n        :param endpoint: the desired endpoint\n        :param request_method: the method (e.g. POST, GET, PATCH, DELETE)\n        :param files: files to send. only used when changing a profile image\n        :param headers: headers for the request. only specified when changing a profile image\n        :return:\n        '
    if (headers is None):
        headers = self._get_headers()
    if (files is None):
        r = requests.request(request_method.value, url=(self.__url + endpoint), data=json.dumps(payload), headers=headers)
    else:
        r = requests.request(request_method.value, url=(self.__url + endpoint), data=payload, files=files, headers=headers)
    try:
        json_content = json.loads(r.content)
    except json.decoder.JSONDecodeError:
        return r
    return json_content
