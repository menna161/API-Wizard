import datetime
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.fly_zone import FlyZone
from auvsi_suas.models.uas_telemetry import UasTelemetry
from auvsi_suas.models.waypoint import Waypoint
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


def test_out_of_bounds(self):
    'Tests the UAS out of bounds method.'
    (zone_details, uas_details) = TESTDATA_FLYZONE_EVALBOUNDS
    zones = []
    for (alt_min, alt_max, wpts) in zone_details:
        zone = FlyZone()
        zone.altitude_msl_min = alt_min
        zone.altitude_msl_max = alt_max
        zone.save()
        for wpt_id in range(len(wpts)):
            (lat, lon) = wpts[wpt_id]
            wpt = Waypoint()
            wpt.order = wpt_id
            wpt.latitude = lat
            wpt.longitude = lon
            wpt.altitude_msl = 0
            wpt.save()
            zone.boundary_pts.add(wpt)
        zone.save()
        zones.append(zone)
    user_id = 0
    epoch = timezone.now().replace(year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    for (exp_violations, exp_out_of_bounds_time, log_details) in uas_details:
        user = User.objects.create_user(('testuser%d' % user_id), 'testemail@x.com', 'testpass')
        user_id += 1
        uas_logs = []
        for (lat, lon, alt, timestamp) in log_details:
            log = UasTelemetry()
            log.user = user
            log.latitude = lat
            log.longitude = lon
            log.altitude_msl = alt
            log.uas_heading = 0
            log.save()
            log.timestamp = (epoch + datetime.timedelta(seconds=timestamp))
            log.save()
            uas_logs.append(log)
        (num_violations, out_of_bounds_time) = FlyZone.out_of_bounds(zones, uas_logs)
        self.assertEqual(num_violations, exp_violations)
        self.assertAlmostEqual(out_of_bounds_time.total_seconds(), exp_out_of_bounds_time)
