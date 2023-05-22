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


def parse(self, from_date: dts=None, usetimezone: bool=False) -> list:
    try:
        json_string = self.json_file.read()
        json_string = re.sub('"partTimeMap"\\:{(.*?)}\\,', '', json_string)
        data = json.loads(json_string)
        for (n, activity_dict) in enumerate(data):
            activity_date = dts.strptime(str(activity_dict['recordDay']), '%Y%m%d')
            if (activity_date >= from_date):
                for y in range(len(activity_dict['motionPathData'])):
                    time_zone = int(activity_dict['motionPathData'][y]['timeZone'])
                    time_offset = (((time_zone / 100) * 60) * 60)
                    datetime_local = time.strftime('%Y%m%d_%H%M%S', time.gmtime(((activity_dict['motionPathData'][y]['startTime'] / 1000) + time_offset)))
                    logging.info('Found activity in JSON at index %d to parse from %s (YYY-MM-DD)', n, activity_date.isoformat())
                    motion_path_data = activity_dict['motionPathData'][y]
                    hitrack_data = motion_path_data['attribute']
                    hitrack_data_add = hitrack_data
                    hitrack_data_add = re.sub('HW_EXT_TRACK_DETAIL\\@is(.*)\\&\\&HW_EXT_TRACK_SIMPLIFY\\@is', '', hitrack_data_add, flags=re.DOTALL)
                    activity_dict_add = json.loads(hitrack_data_add)
                    hitrack_data = re.sub('HW_EXT_TRACK_DETAIL\\@is', '', hitrack_data)
                    hitrack_data = re.sub('\\&\\&HW_EXT_TRACK_SIMPLIFY\\@is(.*)', '', hitrack_data)
                    hitrack_filename = ('%s/HiTrack_%s_%d' % (self.output_dir, datetime_local, n))
                    logging.info('Saving activity at index %d from %s to HiTrack file %s for parsing', n, activity_date, hitrack_filename)
                    try:
                        hitrack_file = open(hitrack_filename, 'w+')
                        hitrack_file.write(hitrack_data)
                    except Exception as e:
                        logging.error('Error saving activity at index %d from %s to HiTrack file for parsing.\n%s', n, activity_date, e)
                    finally:
                        try:
                            if hitrack_file:
                                hitrack_file.close()
                        except Exception as e:
                            logging.error('Error closing HiTrack file <%s>\n', hitrack_filename, e)
                    hitrack_file = HiTrackFile(hitrack_filename)
                    hi_activity = hitrack_file.parse()
                    time_zone = activity_dict['motionPathData'][y]['timeZone']
                    time_zone = ((time_zone[:3] + ':') + time_zone[3:])
                    if usetimezone:
                        hi_activity.JSON_timeZone = time_zone
                        hi_activity.JSON_timeOffset = int(time_offset)
                    if ('swim_pool_length' in activity_dict_add['wearSportData']):
                        hi_activity.JSON_swim_pool_length = (activity_dict_add['wearSportData']['swim_pool_length'] / 100)
                    self.hi_activity_list.append(hi_activity)
            else:
                logging.info('Skipped parsing activity at index %d being an activity from %s before %s (YYYYMMDD).', n, activity_date.isoformat(), from_date.isoformat())
        return self.hi_activity_list
    except Exception as e:
        logging.error('Error parsing JSON file <%s>\n%s', self.json_file.name, e)
        raise Exception('Error parsing JSON file <%s>', self.json_file.name)
