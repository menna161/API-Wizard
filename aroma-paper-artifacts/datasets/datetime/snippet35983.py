import datetime
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.uas_telemetry import UasTelemetry
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def test_infinite_period(self):
    "Can't calculate a rate for an infinite (unbounded) period."
    delta = datetime.timedelta(seconds=1)
    logs = self.create_logs(self.user1, delta=delta)
    period = TimePeriod(None, None)
    self.assertSequenceEqual((None, None), UasTelemetry.rates(self.user1, [period]))
