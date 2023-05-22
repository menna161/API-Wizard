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


def test_GET_CORS_headers_valid_origin():
    valid_origin = 'http://testdomain.com'
    response = requests.get('{}?site={}&path={}'.format(COMMENT_SIDECAR_URL, DEFAULT_SITE, DEFAULT_PATH), headers={'Origin': valid_origin})
    assert_cors_headers_exists(response, valid_origin)
