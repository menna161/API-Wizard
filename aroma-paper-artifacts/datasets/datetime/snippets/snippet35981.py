import datetime
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.uas_telemetry import UasTelemetry
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def test_delayed_start_early_end_logs(self):
    'Rates computed consider time before and after log sequence.'
    delta = datetime.timedelta(seconds=1)
    logs = self.create_logs(self.user1, delta=delta)
    period = self.consistent_period(logs, (delta * 2))
    rates = UasTelemetry.rates(self.user1, [period])
    self.assertSequenceEqual((2, (((1.0 * 9) + (2.0 * 2)) / (9 + 2))), rates)
