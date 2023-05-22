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


def test_subscription_mail_on_reply():
    clear_mails()
    path = '/commented-post/'
    site = 'https://mysupersite.de'
    parent = create_post_payload()
    parent['email'] = 'root@root.com'
    parent['path'] = path
    parent['site'] = site
    response = post_comment(parent)
    parent_id = response.json()['id']
    reply = create_post_payload()
    reply['replyTo'] = parent_id
    reply['path'] = path
    reply['site'] = site
    reply['content'] = 'Root, I disagree!'
    reply['email'] = 'reply@reply.com!'
    reply['author'] = 'Replyer'
    post_comment(reply)
    json = requests.get(MAILHOG_MESSAGES_URL).json()
    assert_that(json['total']).is_greater_than(1)
    mail = find_mail_by_sender(items=json['items'], email_from=reply['author'])
    if (not mail):
        fail('No notification mail was found! recipient/parent: {}. sender/reply author: {}'.format(parent['email'], reply['author']))
    assert_that(mail['from']).contains(reply['author']).does_not_contain(reply['email'])
    assert_that(mail).has_subject('Reply to your comment by {}'.format(reply['author'])).has_to(parent['email'])
    unsubscribe_token = retrieve_unsubscribe_token_from_db(parent_id)
    unsubscribe_link = '{}?commentId={}&unsubscribeToken={}'.format(UNSUBSCRIBE_URL, parent_id, unsubscribe_token)
    link_to_site = '{}{}#comment-sidecar'.format(site, path)
    assert_that(mail['body']).contains(reply['content']).contains(unsubscribe_link).contains(link_to_site).contains(reply['author']).does_not_contain(reply['email'])
