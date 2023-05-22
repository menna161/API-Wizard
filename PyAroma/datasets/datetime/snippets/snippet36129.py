import datetime
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.gps_position import GpsPosition
from auvsi_suas.models.mission_config import MissionConfig
from auvsi_suas.models.uas_telemetry import UasTelemetry
from auvsi_suas.models.waypoint import Waypoint
from auvsi_suas.proto.interop_admin_api_pb2 import WaypointEvaluation
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def create_log_element(self, timestamp, lat, lon, alt, heading, user=None):
    if (user is None):
        user = self.user
    log = UasTelemetry(user=user, latitude=lat, longitude=lon, altitude_msl=alt, uas_heading=heading)
    log.save()
    log.timestamp = (self.now + datetime.timedelta(seconds=timestamp))
    log.save()
    return log
