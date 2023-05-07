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
def satisfied_waypoints(cls, home_pos, waypoints, uas_telemetry_logs):
    'Determines whether the UAS satisfied the waypoints.\n\n        Waypoints must be satisfied in order. The entire pattern may be\n        restarted at any point. The best (most waypoints satisfied) attempt\n        will be returned.\n\n        Assumes that waypoints are at least\n        SATISFIED_WAYPOINT_DIST_MAX_FT apart.\n\n        Args:\n            home_pos: The home position for projections.\n            waypoints: A list of waypoints to check against.\n            uas_telemetry_logs: A list of UAS Telemetry logs to evaluate.\n        Returns:\n            A list of auvsi_suas.proto.WaypointEvaluation.\n        '
    best = {}
    hits = []
    for log in cls.interpolate(uas_telemetry_logs):
        for (iw, waypoint) in enumerate(waypoints):
            dist = log.distance_to(waypoint)
            best[iw] = min(best.get(iw, dist), dist)
            score = pow(max(0, (float((SATISFIED_WAYPOINT_DIST_MAX_FT - dist)) / SATISFIED_WAYPOINT_DIST_MAX_FT)), (1.0 / 3.0))
            if (score > 0):
                hits.append((iw, dist, score))
    hits = [max(g, key=(lambda x: x[2])) for (_, g) in itertools.groupby(hits, (lambda x: x[0]))]
    dp = defaultdict((lambda : defaultdict((lambda : (0, None, None)))))
    highest_total = None
    highest_total_pos = (None, None)
    for iw in range(len(waypoints)):
        for (ih, (hiw, hdist, hscore)) in enumerate(hits):
            score = (hscore if (iw == hiw) else 0.0)
            prev_iw = (iw - 1)
            total_score = score
            total_score_back = (None, None)
            if (prev_iw >= 0):
                for prev_ih in range((ih + 1)):
                    (prev_total_score, _) = dp[prev_iw][prev_ih]
                    new_total_score = (prev_total_score + score)
                    if (new_total_score > total_score):
                        total_score = new_total_score
                        total_score_back = (prev_iw, prev_ih)
            dp[iw][ih] = (total_score, total_score_back)
            if ((highest_total is None) or (total_score > highest_total)):
                highest_total = total_score
                highest_total_pos = (iw, ih)
    scores = defaultdict((lambda : (0, None)))
    cur_pos = highest_total_pos
    while (cur_pos != (None, None)):
        (cur_iw, cur_ih) = cur_pos
        (hiw, hdist, hscore) = hits[cur_ih]
        if (cur_iw == hiw):
            scores[cur_iw] = (hscore, hdist)
        (_, cur_pos) = dp[cur_iw][cur_ih]
    waypoint_evals = []
    for (iw, waypoint) in enumerate(waypoints):
        (score, dist) = scores[iw]
        waypoint_eval = interop_admin_api_pb2.WaypointEvaluation()
        waypoint_eval.id = iw
        waypoint_eval.score_ratio = score
        if (dist is not None):
            waypoint_eval.closest_for_scored_approach_ft = dist
        if (iw in best):
            waypoint_eval.closest_for_mission_ft = best[iw]
        waypoint_evals.append(waypoint_eval)
    return waypoint_evals
