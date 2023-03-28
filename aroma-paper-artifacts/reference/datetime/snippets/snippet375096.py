import subprocess
import os
import time
import core
import config
import rss
from datetime import datetime, timedelta
from core import Recording


def updatePass():
    passes = list()
    timenow = datetime.utcnow()
    for satellite in config.satellites:
        predictor = satellite.getPredictor()
        next_pass = predictor.get_next_pass(config.location, max_elevation_gt=satellite.min_elevation)
        max_elevation = next_pass.max_elevation_deg
        priority = satellite.priority
        if (next_pass.aos < (timenow + timedelta(hours=1))):
            passes.append([next_pass, satellite, max_elevation, priority])
    for current_pass in passes:
        current_pass_obj = current_pass[0]
        current_sat_obj = current_pass[1]
        current_max_ele = current_pass[2]
        current_priority = current_pass[3]
        keep = True
        keep_modified = False
        custom_aos = 0
        custom_los = 0
        for (next_pass, satellite, max_elevation, priority) in passes:
            if (next_pass == current_pass_obj):
                continue
            if ((next_pass.aos <= current_pass_obj.los) and (not (next_pass.los <= current_pass_obj.aos))):
                if (current_priority == priority):
                    if (current_max_ele < max_elevation):
                        keep = False
                        overlapping_time = (current_pass_obj.los - next_pass.aos)
                        if (overlapping_time < timedelta(minutes=config.maximum_overlap)):
                            keep_modified = True
                            custom_aos = current_pass_obj.aos
                            custom_los = next_pass.aos
                elif (current_priority < priority):
                    keep = False
                    overlapping_time = (current_pass_obj.los - next_pass.aos)
                    if (overlapping_time < timedelta(minutes=config.maximum_overlap)):
                        keep_modified = True
                        custom_aos = current_pass_obj.aos
                        custom_los = next_pass.aos
        if keep:
            schedulePass(current_pass_obj, current_sat_obj)
        elif keep_modified:
            schedulePass(current_pass_obj, current_sat_obj, custom_aos=custom_aos, custom_los=custom_los)
