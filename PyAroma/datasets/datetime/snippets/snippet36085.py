import datetime
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.gps_position import GpsPosition
from auvsi_suas.models.mission_config import MissionConfig
from auvsi_suas.models.takeoff_or_landing_event import TakeoffOrLandingEvent
from auvsi_suas.models.time_period import TimePeriod
from auvsi_suas.models.waypoint import Waypoint
from auvsi_suas.models.access_log_test import TestAccessLogMixinCommon


def setUp(self):
    super(TestTakeoffOrLandingEventModel, self).setUp()
    pos = GpsPosition()
    pos.latitude = 10
    pos.longitude = 100
    pos.save()
    apos = AerialPosition()
    apos.latitude = 10
    apos.longitude = 100
    apos.altitude_msl = 1000
    apos.save()
    wpt = Waypoint()
    wpt.latitude = 10
    wpt.longitude = 100
    wpt.altitude_msl = 1000
    wpt.order = 10
    wpt.save()
    self.mission = MissionConfig()
    self.mission.home_pos = pos
    self.mission.lost_comms_pos = pos
    self.mission.emergent_last_known_pos = pos
    self.mission.off_axis_odlc_pos = pos
    self.mission.map_center_pos = pos
    self.mission.map_height_ft = 1
    self.mission.air_drop_pos = pos
    self.mission.ugv_drive_pos = pos
    self.mission.save()
    self.mission.mission_waypoints.add(wpt)
    self.mission.search_grid_points.add(wpt)
    self.mission.save()
    self.mission2 = MissionConfig()
    self.mission2.home_pos = pos
    self.mission2.lost_comms_pos = pos
    self.mission2.emergent_last_known_pos = pos
    self.mission2.off_axis_odlc_pos = pos
    self.mission2.map_center_pos = pos
    self.mission2.map_height_ft = 1
    self.mission2.air_drop_pos = pos
    self.mission2.ugv_drive_pos = pos
    self.mission2.save()
    self.mission2.mission_waypoints.add(wpt)
    self.mission2.search_grid_points.add(wpt)
    self.mission2.save()
    self.ten_minutes = datetime.timedelta(minutes=10)
