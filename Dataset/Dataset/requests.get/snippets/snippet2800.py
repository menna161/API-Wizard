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


@pytest.mark.parametrize('queryParams', {'', 'site=&path=', 'site=domain.com', 'path=blogpost1'})
def test_GET_invalid_query_params(queryParams):
    response = requests.get(f'{COMMENT_SIDECAR_URL}?{queryParams}')
    assert_that(response.status_code).is_equal_to(400)
    assert_that(response.json()['message']).is_equal_to(ERROR_MESSAGE_MISSING_SITE_PATH)
