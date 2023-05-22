import requests
import time
import json
import re
import logging, os, sys
from ..utils import SSH


def _create(self, url, data, retry_when_response_unexpected_strings=None, retry_until_response_expected_strings=None):
    return self._request(url, method=requests.post, data=data, retry_when_response_unexpected_strings=retry_when_response_unexpected_strings, retry_until_response_expected_strings=retry_until_response_expected_strings)
