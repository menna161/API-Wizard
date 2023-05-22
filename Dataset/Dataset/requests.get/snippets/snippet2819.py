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


def test_no_email_notification_after_invalid_POST():
    clear_mails()
    post_payload = create_post_payload()
    post_payload.pop('author')
    post_comment(post_payload, assert_success=False)
    json = requests.get(MAILHOG_MESSAGES_URL).json()
    assert_that(json['total']).is_equal_to(0)
