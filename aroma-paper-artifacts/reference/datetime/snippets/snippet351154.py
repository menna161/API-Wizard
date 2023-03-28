import random
import unittest
from datetime import datetime, timedelta
import os, sys
import tests.models
from arxivtimes_indicator.models.model import *


def generate_data(self):
    LABELS = list(IndicatorApi.LABEL_TO_GENRE.keys())
    url = 'http://example.com'
    title = 'example'
    body = 'example'
    user_id = 'user_{}'.format(random.randint(0, 10))
    avatar_url = 'http://example.com'
    labels = [Label(name=name) for name in random.sample(LABELS, random.randint(1, 4))]
    score = random.randint(30, 80)
    now = datetime.now()
    delta = timedelta(weeks=random.randint(1, 25))
    created_at = '{}-{} 00:00:00+00:00'.format((now - delta).strftime('%Y-%m'), random.randint(1, 28))
    issue = Issue(title=title, url=url, user_id=user_id, avatar_url=avatar_url, score=score, created_at=created_at, body=body, labels=labels)
    return (issue, labels)
