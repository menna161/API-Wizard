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


def test_email_notification_after_successful_POST():
    clear_mails()
    post_payload = create_post_payload()
    post_comment(post_payload)
    json = requests.get(MAILHOG_MESSAGES_URL).json()
    assert_that(json['total']).is_equal_to(1)
    mail_content = json['items'][0]['Content']
    mail_body = mail_content['Body']
    assert_that(mail_body).contains(post_payload['site']).contains(post_payload['path']).contains(post_payload['content'])
    headers = mail_content['Headers']
    assert_that(headers['Content-Transfer-Encoding'][0]).is_equal_to('8bit')
    assert_that(headers['Content-Type'][0]).is_equal_to('text/plain; charset=UTF-8')
    assert_that(headers['Mime-Version'][0]).is_equal_to('1.0')
    assert_that(headers['From'][0]).is_equal_to('{}<{}>'.format(post_payload['author'], post_payload['email']))
    assert_that(headers['Subject'][0]).is_equal_to('Comment by {} on {}'.format(post_payload['author'], post_payload['path']))
    assert_that(headers['To'][0]).is_equal_to(ADMIN_EMAIL)
