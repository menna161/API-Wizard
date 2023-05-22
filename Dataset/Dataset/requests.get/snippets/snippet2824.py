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


def test_subscription_no_mail_on_reply_if_unsubscribed():
    clear_mails()
    root_payload = create_post_payload()
    root_payload['email'] = 'root@root.com'
    response = post_comment(root_payload)
    root_id = response.json()['id']
    unsubscribe_token = retrieve_unsubscribe_token_from_db(root_id)
    unsubscribe(root_id, unsubscribe_token)
    reply_payload = create_post_payload()
    reply_payload['replyTo'] = root_id
    reply_payload['content'] = 'Root, I disagree!'
    reply_payload['email'] = 'reply@reply.com!'
    reply_payload['author'] = 'Replyer'
    post_comment(reply_payload)
    json = requests.get(MAILHOG_MESSAGES_URL).json()
    assert_no_mail_except_admin_mail(items=json['items'])
