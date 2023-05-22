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


def _generate_swim_xml_data(self, el_activity):
    ' Generates the TCX XML content for swimming activities '
    cumulative_distance = 0
    for (n, lap) in enumerate(self.hi_activity.get_swim_data()):
        el_lap = xml_et.SubElement(el_activity, 'Lap')
        el_lap.set('StartTime', (((lap['start'] + datetime.timedelta(seconds=self.hi_activity.JSON_timeOffset)).isoformat('T', 'seconds') + '.000') + self.hi_activity.JSON_timeZone))
        el_total_time_seconds = xml_et.SubElement(el_lap, 'TotalTimeSeconds')
        el_total_time_seconds.text = str(lap['duration'])
        el_distance_meters = xml_et.SubElement(el_lap, 'DistanceMeters')
        el_distance_meters.text = str(lap['distance'])
        el_calories = xml_et.SubElement(el_lap, 'Calories')
        el_calories.text = '0'
        el_intensity = xml_et.SubElement(el_lap, 'Intensity')
        el_intensity.text = 'Active'
        el_trigger_method = xml_et.SubElement(el_lap, 'TriggerMethod')
        el_trigger_method.text = 'Manual'
        el_track = xml_et.SubElement(el_lap, 'Track')
        el_trackpoint = xml_et.SubElement(el_track, 'Trackpoint')
        el_time = xml_et.SubElement(el_trackpoint, 'Time')
        el_time.text = (((lap['start'] + datetime.timedelta(seconds=self.hi_activity.JSON_timeOffset)).isoformat('T', 'seconds') + '.000') + self.hi_activity.JSON_timeZone)
        el_distance_meters = xml_et.SubElement(el_trackpoint, 'DistanceMeters')
        el_distance_meters.text = str(cumulative_distance)
        for (i, lap_detail_data) in enumerate(self.hi_activity.get_segment_data(self.hi_activity.get_segments()[n])):
            if ('lat' in lap_detail_data):
                el_trackpoint = xml_et.SubElement(el_track, 'Trackpoint')
                el_time = xml_et.SubElement(el_trackpoint, 'Time')
                el_time.text = (((lap_detail_data['t'] + datetime.timedelta(seconds=self.hi_activity.JSON_timeOffset)).isoformat('T', 'seconds') + '.000') + self.hi_activity.JSON_timeZone)
                el_position = xml_et.SubElement(el_trackpoint, 'Position')
                el_latitude_degrees = xml_et.SubElement(el_position, 'LatitudeDegrees')
                el_latitude_degrees.text = str(lap_detail_data['lat'])
                el_longitude_degrees = xml_et.SubElement(el_position, 'LongitudeDegrees')
                el_longitude_degrees.text = str(lap_detail_data['lon'])
        cumulative_distance += lap['distance']
        el_trackpoint = xml_et.SubElement(el_track, 'Trackpoint')
        el_time = xml_et.SubElement(el_trackpoint, 'Time')
        el_time.text = (((lap['stop'] + datetime.timedelta(seconds=self.hi_activity.JSON_timeOffset)).isoformat('T', 'seconds') + '.000') + self.hi_activity.JSON_timeZone)
        el_distance_meters = xml_et.SubElement(el_trackpoint, 'DistanceMeters')
        el_distance_meters.text = str(cumulative_distance)
    return
