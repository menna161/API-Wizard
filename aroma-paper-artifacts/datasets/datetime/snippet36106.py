import collections
import datetime
import functools
import json
import logging
import os
import random
from auvsi_suas.models.aerial_position import AerialPosition
from auvsi_suas.models.fly_zone import FlyZone
from auvsi_suas.models.gps_position import GpsPosition
from auvsi_suas.models.map import Map
from auvsi_suas.models.mission_config import MissionConfig
from auvsi_suas.models.mission_judge_feedback import MissionJudgeFeedback
from auvsi_suas.models.odlc import Odlc
from auvsi_suas.models.stationary_obstacle import StationaryObstacle
from auvsi_suas.models.takeoff_or_landing_event import TakeoffOrLandingEvent
from auvsi_suas.models.waypoint import Waypoint
from auvsi_suas.proto import interop_admin_api_pb2
from auvsi_suas.proto import interop_api_pb2
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from google.protobuf import json_format


def simulate_team_mission(test, mission, superuser, user):
    "Simulates a team's mission demonstration.\n\n    Args:\n        test: The test case.\n        mission: The mission to simulate for.\n        superuser: The superuser for admin actions.\n        user: The user for the team.\n    "
    total_telem = 100
    waypoints_hit = len(mission.mission_waypoints.all())
    odlcs_correct = len(mission.odlcs.all())
    odlcs_incorrect = 1
    c = Client()
    c.force_login(user)
    TakeoffOrLandingEvent(user=user, mission=mission, uas_in_air=True).save()
    for i in range(total_telem):
        simulate_telemetry(test, client=c, mission=mission, hit_waypoint=(i < waypoints_hit))
    t = TakeoffOrLandingEvent(user=user, mission=mission, uas_in_air=False)
    t.timestamp = (timezone.now() + datetime.timedelta(seconds=5))
    t.save()
    for _ in range(odlcs_correct):
        simulate_odlc(test, c, mission, actual=True)
    for _ in range(odlcs_incorrect):
        simulate_odlc(test, c, mission, actual=False)
    simulate_map(test, c, mission, user)
    feedback = MissionJudgeFeedback()
    feedback.mission = mission
    feedback.user = user
    feedback.flight_time = datetime.timedelta(seconds=1)
    feedback.post_process_time = datetime.timedelta(seconds=1)
    feedback.used_timeout = False
    feedback.min_auto_flight_time = True
    feedback.safety_pilot_takeovers = 1
    feedback.out_of_bounds = False
    feedback.things_fell_off_uas = 0
    feedback.crashed = False
    feedback.air_drop_accuracy = interop_admin_api_pb2.MissionJudgeFeedback.WITHIN_15_FT
    feedback.ugv_drove_to_location = True
    feedback.operational_excellence_percent = 90
    feedback.save()
    c = Client()
    c.force_login(superuser)
    review_data = json.loads(c.get(odlcs_review_url).content)
    for odlc_review in review_data:
        pk = int(odlc_review['odlc']['id'])
        review = interop_admin_api_pb2.OldcReview()
        review.odlc.id = pk
        review.thumbnail_approved = True
        review.description_approved = True
        r = client.put(odlc_review_id_url(args=[pk]), data=json_format.MessageToJson(review), content_type='application/json')
        test.assertEqual(r.status_code, 200, r.content)
    m = Map.objects.get(mission_id=mission.pk, user_id=user.pk)
    m.quality = interop_admin_api_pb2.MapEvaluation.MapQuality.MEDIUM
    m.save()
