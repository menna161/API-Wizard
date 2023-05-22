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


def unsubscribe_with_url_assert_error(url):
    response = requests.get(url)
    assert_that(response).has_status_code(400)
    assert_that(response.json()['message']).is_equal_to(INVALID_QUERY_PARAMS_UNSUBSCRIBE)
