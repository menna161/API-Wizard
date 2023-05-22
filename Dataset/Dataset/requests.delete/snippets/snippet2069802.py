import requests
import time
import json
import re
import logging, os, sys
from ..utils import SSH


def _delete(self, url, retry_when_response_unexpected_strings=None, retry_until_response_expected_strings=None):
    try:
        return self._request(url, method=requests.delete, retry_when_response_unexpected_strings=retry_when_response_unexpected_strings, retry_until_response_expected_strings=retry_until_response_expected_strings)
    except Exception as e:
        if (e.args[0] != 404):
            raise e
