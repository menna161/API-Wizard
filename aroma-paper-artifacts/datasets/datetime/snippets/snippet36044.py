import datetime
from auvsi_suas.proto import interop_admin_api_pb2
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.gps_position import GpsPosition
from auvsi_suas.models.mission_config import MissionConfig
from auvsi_suas.models.mission_judge_feedback import MissionJudgeFeedback
from auvsi_suas.models.waypoint import Waypoint
from django.contrib.auth.models import User
from django.test import TestCase


def setUp(self):
    pos = GpsPosition()
    pos.latitude = 10
    pos.longitude = 100
    pos.save()
    wpt = Waypoint()
    wpt.order = 10
    wpt.latitude = 10
    wpt.longitude = 100
    wpt.altitude_msl = 1000
    wpt.save()
    config = MissionConfig()
    config.home_pos = pos
    config.lost_comms_pos = pos
    config.emergent_last_known_pos = pos
    config.off_axis_odlc_pos = pos
    config.map_center_pos = pos
    config.map_height_ft = 1
    config.air_drop_pos = pos
    config.ugv_drive_pos = pos
    config.save()
    config.mission_waypoints.add(wpt)
    config.search_grid_points.add(wpt)
    config.save()
    user = User.objects.create_user('user', 'email@example.com', 'pass')
    self.feedback = MissionJudgeFeedback(mission=config, user=user, flight_time=datetime.timedelta(seconds=1), post_process_time=datetime.timedelta(seconds=2), used_timeout=True, min_auto_flight_time=True, safety_pilot_takeovers=3, out_of_bounds=True, things_fell_off_uas=False, crashed=False, air_drop_accuracy=interop_admin_api_pb2.MissionJudgeFeedback.WITHIN_05_FT, ugv_drove_to_location=False, operational_excellence_percent=9)
    self.feedback.save()
