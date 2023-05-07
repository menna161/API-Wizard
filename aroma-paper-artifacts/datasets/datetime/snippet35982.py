import datetime
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.uas_telemetry import UasTelemetry
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def test_provided_logs(self):
    'Rates computed with provided logs only.'
    delta = datetime.timedelta(seconds=1)
    used_logs = self.create_logs(self.user1, delta=delta)
    unused_logs = self.create_logs(self.user1, delta=delta)
    period = self.consistent_period(used_logs, delta)
    rates = UasTelemetry.rates(self.user1, [period], time_period_logs=[used_logs])
    self.assertSequenceEqual((1, 1), rates)
