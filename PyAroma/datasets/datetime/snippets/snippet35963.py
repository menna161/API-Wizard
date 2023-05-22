import datetime
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.uas_telemetry import UasTelemetry
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def test_no_data(self):
    self.assertEqual(None, UasTelemetry.last_for_user(self.user1))
    self.assertEqual(0, len(UasTelemetry.by_user(self.user1)))
    self.assertSequenceEqual([], UasTelemetry.by_time_period(self.user1, []))
    self.assertTupleEqual((None, None), UasTelemetry.rates(self.user1, []))
    start = timezone.now()
    delta = datetime.timedelta(seconds=10)
    time_period_sets = [[TimePeriod(start, (start + delta))], [TimePeriod(start, (start + delta)), TimePeriod((start + delta), (start + (delta * 2)))]]
    for time_periods in time_period_sets:
        for logs in UasTelemetry.by_time_period(self.user1, time_periods):
            self.assertEqual(0, len(logs))
        self.assertTupleEqual((delta.total_seconds(), delta.total_seconds()), UasTelemetry.rates(self.user1, time_periods))
    time_period_sets = [[], [TimePeriod(None, start)], [TimePeriod((start + delta), None)], [TimePeriod(None, start), TimePeriod(start, (start + delta)), TimePeriod((start + delta), None)]]
    for time_periods in time_period_sets:
        for logs in UasTelemetry.by_time_period(self.user1, time_periods):
            self.assertEqual(0, len(logs))
        self.assertTupleEqual((None, None), UasTelemetry.rates(self.user1, time_periods))
