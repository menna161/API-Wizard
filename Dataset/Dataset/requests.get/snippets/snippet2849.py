import re
import pytest
import requests
from mysql.connector import connect
from requests.models import Response
import unittest
import hashlib
import time
from path import Path
from assertpy import assert_that, fail


def get_comments(site: str=DEFAULT_SITE, path: str=DEFAULT_PATH, assert_success: bool=True) -> Response:
    response = requests.get('{}?site={}&path={}'.format(COMMENT_SIDECAR_URL, site, path))
    if assert_success:
        assert_that(response.status_code).described_as(('Getting comments failed. Message: ' + response.text)).is_equal_to(200)
    return response
