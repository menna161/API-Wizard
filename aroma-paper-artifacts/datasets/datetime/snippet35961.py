import datetime
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.uas_telemetry import UasTelemetry
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def setUp(self):
    'Sets up the tests.'
    self.user1 = User.objects.create_user('user1', 'email@example.com', 'pass')
    self.user2 = User.objects.create_user('user2', 'email@example.com', 'pass')
    self.year2000 = datetime.datetime(2000, 1, 1, tzinfo=timezone.utc)
    self.year2001 = datetime.datetime(2001, 1, 1, tzinfo=timezone.utc)
    self.year2002 = datetime.datetime(2002, 1, 1, tzinfo=timezone.utc)
    self.year2003 = datetime.datetime(2003, 1, 1, tzinfo=timezone.utc)
    self.year2004 = datetime.datetime(2004, 1, 1, tzinfo=timezone.utc)
