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


def clear_mails():
    response = requests.delete((MAILHOG_BASE_URL + 'v1/messages'))
    assert_that(response.status_code).described_as("Test setup failed: Couldn't delete mails in mailhog.").is_equal_to(200)
