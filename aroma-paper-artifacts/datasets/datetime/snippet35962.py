import datetime
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.uas_telemetry import UasTelemetry
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def create_logs(self, user, num=10, start=None, delta=None):
    if (start is None):
        start = timezone.now()
    if (delta is None):
        delta = datetime.timedelta(seconds=1)
    logs = []
    for i in range(num):
        log = UasTelemetry(user=user, latitude=0, longitude=0, altitude_msl=0, uas_heading=0.0)
        log.save()
        log.timestamp = (start + (i * delta))
        log.save()
        logs.append(log)
    return logs
