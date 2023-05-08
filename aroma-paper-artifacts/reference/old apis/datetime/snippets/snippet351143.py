import random
import unittest
from datetime import datetime, timedelta
import os, sys
import tests.models
from arxivtimes_indicator.models.model import *


def test_create(self):
    title = 'test_title'
    url = 'https://github.com/arXivTimes/arXivTimes/issues/350'
    user_id = 'icoxfog417'
    avatar_url = 'https://avatars2.githubusercontent.com/u/544269?v=3'
    score = 55
    created_at = datetime.now()
    body = 'test_body'
    labels = [Label(name='ComputerVision'), Label(name='CNN')]
    issue = Issue(title=title, url=url, user_id=user_id, avatar_url=avatar_url, score=score, created_at=created_at, body=body, labels=labels)
    self.assertEqual(issue.title, title)
    self.assertEqual(issue.url, url)
    self.assertEqual(issue.user_id, user_id)
    self.assertEqual(issue.avatar_url, avatar_url)
    self.assertEqual(issue.score, score)
    self.assertEqual(issue.created_at, created_at)
    self.assertEqual(issue.body, body)
    self.assertEqual(issue.labels, labels)
