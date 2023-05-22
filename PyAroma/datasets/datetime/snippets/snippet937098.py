import argparse
import collections
import csv
import datetime
import json
import logging
import math
import operator
import os
import re
import sys
import tarfile
import tempfile
import time
import urllib.request as url_req
import xml.etree.cElementTree as xml_et
from datetime import datetime as dts
from datetime import timedelta as dts_delta
from typing import List, Optional
import xmlschema


def _generate_walk_run_cycle_xml_data(self, el_activity):
    for (n, segment) in enumerate(self.hi_activity.get_segments()):
        el_lap = xml_et.SubElement(el_activity, 'Lap')
        el_lap.set('StartTime', (((segment['start'] + datetime.timedelta(seconds=self.hi_activity.JSON_timeOffset)).isoformat('T', 'seconds') + '.000') + self.hi_activity.JSON_timeZone))
        el_total_time_seconds = xml_et.SubElement(el_lap, 'TotalTimeSeconds')
        el_total_time_seconds.text = str(segment['duration'])
        el_distance_meters = xml_et.SubElement(el_lap, 'DistanceMeters')
        el_distance_meters.text = str(segment['distance'])
        el_calories = xml_et.SubElement(el_lap, 'Calories')
        el_calories.text = '0'
        el_intensity = xml_et.SubElement(el_lap, 'Intensity')
        el_intensity.text = 'Active'
        el_trigger_method = xml_et.SubElement(el_lap, 'TriggerMethod')
        el_trigger_method.text = 'Manual'
        el_track = xml_et.SubElement(el_lap, 'Track')
        segment_data = self.hi_activity.get_segment_data(segment)
        for data in segment_data:
            el_trackpoint = xml_et.SubElement(el_track, 'Trackpoint')
            el_time = xml_et.SubElement(el_trackpoint, 'Time')
            el_time.text = (((data['t'] + datetime.timedelta(seconds=self.hi_activity.JSON_timeOffset)).isoformat('T', 'seconds') + '.000') + self.hi_activity.JSON_timeZone)
            if ('lat' in data):
                el_position = xml_et.SubElement(el_trackpoint, 'Position')
                el_latitude_degrees = xml_et.SubElement(el_position, 'LatitudeDegrees')
                el_latitude_degrees.text = str(data['lat'])
                el_longitude_degrees = xml_et.SubElement(el_position, 'LongitudeDegrees')
                el_longitude_degrees.text = str(data['lon'])
            if ('alti' in data):
                el_altitude_meters = xml_et.SubElement(el_trackpoint, 'AltitudeMeters')
                el_altitude_meters.text = str(data['alti'])
            if ('distance' in data):
                el_distance_meters = xml_et.SubElement(el_trackpoint, 'DistanceMeters')
                el_distance_meters.text = str(data['distance'])
            if ('hr' in data):
                el_heart_rate_bpm = xml_et.SubElement(el_trackpoint, 'HeartRateBpm')
                el_heart_rate_bpm.set('xsi:type', 'HeartRateInBeatsPerMinute_t')
                value = xml_et.SubElement(el_heart_rate_bpm, 'Value')
                value.text = str(data['hr'])
            if ('s-r' in data):
                if (self.hi_activity.get_activity_type() in (HiActivity.TYPE_WALK, HiActivity.TYPE_RUN)):
                    el_extensions = xml_et.SubElement(el_trackpoint, 'Extensions')
                    el_tpx = xml_et.SubElement(el_extensions, 'TPX')
                    el_tpx.set('xmlns', 'http://www.garmin.com/xmlschemas/ActivityExtension/v2')
                    el_run_cadence = xml_et.SubElement(el_tpx, 'RunCadence')
                    el_run_cadence.text = str(int((data['s-r'] / 2)))
