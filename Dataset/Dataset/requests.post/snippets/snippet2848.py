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


def post_comment(post_payload, assert_success: bool=True) -> Response:
    response = requests.post(url=COMMENT_SIDECAR_URL, json=post_payload)
    if assert_success:
        assert_that(response.status_code).described_as(('Comment creation failed. Message: ' + response.text)).is_equal_to(201)
    return response
