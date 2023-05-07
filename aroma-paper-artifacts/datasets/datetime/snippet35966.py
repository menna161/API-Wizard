import datetime
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.uas_telemetry import UasTelemetry
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def test_by_user_time_restrict(self):
    start = timezone.now()
    delta = datetime.timedelta(seconds=1)
    expect_logs = self.create_logs(self.user1, num=10, start=start, delta=delta)
    logs = UasTelemetry.by_user(self.user1, start_time=start, end_time=(start + (delta * 10)))
    self.assertSequenceEqual(expect_logs, logs)
    logs = UasTelemetry.by_user(self.user1, start_time=(start + (delta * 11)))
    self.assertSequenceEqual([], logs)
    logs = UasTelemetry.by_user(self.user1, end_time=start)
    self.assertSequenceEqual([], logs)
