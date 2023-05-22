import requests
import unittest
from assertpy import assert_that


def test_use_gzip():
    response = requests.get(COMMENT_SIDECAR_URL)
    assert_that(response.headers['Content-Encoding']).is_equal_to('gzip')
