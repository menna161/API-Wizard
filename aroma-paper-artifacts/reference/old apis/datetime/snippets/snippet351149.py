import random
import unittest
from datetime import datetime, timedelta
import os, sys
import tests.models
from arxivtimes_indicator.models.model import *


def test_count(self):
    self.assertEqual(len(Label.select()), 0)
    label = Label(name='example')
    issue = Issue(title='title', url='url', user_id='user_id', avatar_url='avatar_url', score=50, created_at=datetime.now(), body='body', labels=[label])
    issue.save()
    label.issue = issue
    label.save()
    self.assertEqual(len(Label.select()), 1)
    self.assertEqual(len(Issue.select()), 1)