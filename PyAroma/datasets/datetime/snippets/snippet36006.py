import datetime
import logging
import numpy as np
from auvsi_suas.models import aerial_position
from auvsi_suas.models.waypoint import Waypoint
from django.contrib import admin
from django.core import exceptions
from django.core import validators
from django.db import models
from matplotlib import path as mplpath


@classmethod
def out_of_bounds(cls, fly_zones, uas_telemetry_logs):
    'Determines amount of time spent out of bounds.\n\n        Args:\n            fly_zones: The list of FlyZone that the UAS must be in.\n            uas_telemetry_logs: A list of UasTelemetry logs sorted by timestamp\n                which demonstrate the flight of the UAS.\n        Returns:\n            num_violations: The number of times fly zone boundaries violated.\n            total_time: The timedelta for time spent out of bounds\n                as indicated by the telemetry logs.\n        '
    aerial_pos_list = uas_telemetry_logs
    log_ids_to_process = range(len(aerial_pos_list))
    for zone in fly_zones:
        if (len(log_ids_to_process) == 0):
            break
        cur_positions = [aerial_pos_list[cur_id] for cur_id in log_ids_to_process]
        satisfied_positions = zone.contains_many_pos(cur_positions)
        log_ids_to_process = [log_ids_to_process[cur_id] for cur_id in range(len(log_ids_to_process)) if (not satisfied_positions[cur_id])]
    out_of_bounds_time = datetime.timedelta()
    violations = 0
    prev_event_id = (- 1)
    currently_in_bounds = True
    out_of_bounds_ids = set(log_ids_to_process)
    for i in range(len(aerial_pos_list)):
        i_in_bounds = (i not in out_of_bounds_ids)
        if (currently_in_bounds and (not i_in_bounds)):
            currently_in_bounds = False
            violations += 1
            prev_event_id = i
        elif ((not currently_in_bounds) and i_in_bounds):
            time_diff = (uas_telemetry_logs[i].timestamp - uas_telemetry_logs[prev_event_id].timestamp)
            currently_in_bounds = (time_diff.total_seconds() >= OUT_OF_BOUNDS_DEBOUNCE_SEC)
        if ((not currently_in_bounds) and (i > 0)):
            time_diff = (uas_telemetry_logs[i].timestamp - uas_telemetry_logs[(i - 1)].timestamp)
            out_of_bounds_time += time_diff
    return (violations, out_of_bounds_time)
