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


def unsubscribe(comment_id, unsubscribe_token):
    response = requests.get(url='{}?commentId={}&unsubscribeToken={}&XDEBUG_SESSION_START=IDEA_DEBUG'.format(UNSUBSCRIBE_URL, comment_id, unsubscribe_token))
    assert_that(response).has_status_code(200)
    return response
