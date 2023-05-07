import datetime
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.uas_telemetry import UasTelemetry
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def test_different_deltas(self):
    'Sets of logs are combined for overall rates.'
    delta = datetime.timedelta(seconds=1)
    logs = [self.create_logs(self.user1, num=1000, start=self.year2000, delta=delta), self.create_logs(self.user1, num=1000, start=self.year2001, delta=(delta / 2))]
    periods = [self.consistent_period(l, delta) for l in logs]
    rates = UasTelemetry.rates(self.user1, periods)
    self.assertAlmostEqual(1.0, rates[0])
    self.assertAlmostEqual(0.75, rates[1], delta=0.001)
