import datetime
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.uas_telemetry import UasTelemetry
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def test_non_constant_rate(self):
    'Rates computed correctly when non-constant.'
    delta = datetime.timedelta(seconds=1)
    start = timezone.now()
    self.create_logs(self.user1, num=10, start=start, delta=delta)
    self.create_logs(self.user1, num=10, start=(start + (10 * delta)), delta=(2 * delta))
    period = TimePeriod((start - delta), ((start + (10 * delta)) + (10 * (2 * delta))))
    rates = UasTelemetry.rates(self.user1, [period])
    self.assertSequenceEqual((2, (((1.0 * 11) + (2.0 * 10)) / (11 + 10))), rates)
