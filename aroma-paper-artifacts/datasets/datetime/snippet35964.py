import datetime
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.uas_telemetry import UasTelemetry
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def test_basic_access(self):
    start = (timezone.now() - datetime.timedelta(seconds=10))
    logs = self.create_logs(self.user1, start=start)
    log = UasTelemetry.last_for_user(self.user1)
    self.assertEqual(logs[(- 1)], log)
    results = UasTelemetry.by_user(self.user1)
    self.assertSequenceEqual(logs, results)
