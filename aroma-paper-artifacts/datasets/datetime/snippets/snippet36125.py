import datetime
import itertools
import logging
from auvsi_suas.models.access_log import AccessLogMixin
from auvsi_suas.models.aerial_position import AerialPositionMixin
from auvsi_suas.models.gps_position import GpsPosition
from auvsi_suas.proto import interop_admin_api_pb2
from collections import defaultdict
from django.contrib import admin
from django.core import validators
from django.db import models


@classmethod
def interpolate(cls, uas_telemetry_logs, step=TELEMETRY_INTERPOLATION_STEP, max_gap=TELEMETRY_INTERPOLATION_MAX_GAP):
    'Interpolates the ordered set of telemetry.\n\n        Args:\n            uas_telemetry_logs: The telemetry to interpolate.\n            step: The discrete interpolation step in seconds.\n            max_gap: The max time between telemetry to interpolate.\n        Returns:\n            An iterable set of telemetry.\n        '
    for (ix, log) in enumerate(uas_telemetry_logs):
        (yield log)
        if ((ix + 1) >= len(uas_telemetry_logs)):
            continue
        next_log = uas_telemetry_logs[(ix + 1)]
        dt = (next_log.timestamp - log.timestamp)
        if ((dt > max_gap) or (dt <= datetime.timedelta(seconds=0))):
            continue
        t = (log.timestamp + step)
        while (t < next_log.timestamp):
            n_w = ((t - log.timestamp).total_seconds() / dt.total_seconds())
            w = ((next_log.timestamp - t).total_seconds() / dt.total_seconds())
            weighted_avg = (lambda v, n_v: ((w * v) + (n_w * n_v)))
            telem = UasTelemetry()
            telem.user = log.user
            telem.timestamp = t
            telem.latitude = weighted_avg(log.latitude, next_log.latitude)
            telem.longitude = weighted_avg(log.longitude, next_log.longitude)
            telem.altitude_msl = weighted_avg(log.altitude_msl, next_log.altitude_msl)
            telem.uas_heading = weighted_avg(log.uas_heading, next_log.uas_heading)
            (yield telem)
            t += step
