import datetime
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.uas_telemetry import UasTelemetry
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def test_no_logs(self):
    'Test behavior when no logs are present.'
    delta = datetime.timedelta(seconds=10)
    self.assertSequenceEqual((10, 10), UasTelemetry.rates(self.user1, [TimePeriod(self.year2000, (self.year2000 + delta))]))
