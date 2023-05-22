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


def generate_xml(self) -> xml_et.Element:
    '"Generates the TCX XML content.'
    logging.debug('Generating TCX XML data for activity %s', self.hi_activity.activity_id)
    try:
        training_center_database = xml_et.Element('TrainingCenterDatabase')
        training_center_database.set('xsi:schemaLocation', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd')
        training_center_database.set('xmlns', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
        training_center_database.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
        training_center_database.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        training_center_database.set('xmlns:ns3', 'http://www.garmin.com/xmlschemas/ActivityExtension/v2')
        el_activities = xml_et.SubElement(training_center_database, 'Activities')
        el_activity = xml_et.SubElement(el_activities, 'Activity')
        sport = ''
        try:
            sport = [item[1] for item in self._SPORT_TYPES if (item[0] == self.hi_activity.get_activity_type())][0]
        finally:
            if (sport == ''):
                logging.warning('Activity <%s> has an undetermined/unknown sport type.', self.hi_activity.activity_id)
                sport = self._SPORT_OTHER
        el_activity.set('Sport', sport)
        el_id = xml_et.SubElement(el_activity, 'Id')
        el_id.text = (((self.hi_activity.start + datetime.timedelta(seconds=self.hi_activity.JSON_timeOffset)).isoformat('T', 'seconds') + '.000') + self.hi_activity.JSON_timeZone)
        if (self.hi_activity.get_activity_type() in [HiActivity.TYPE_WALK, HiActivity.TYPE_RUN, HiActivity.TYPE_CYCLE, HiActivity.TYPE_UNKNOWN]):
            self._generate_walk_run_cycle_xml_data(el_activity)
        elif (self.hi_activity.get_activity_type() in [HiActivity.TYPE_POOL_SWIM, HiActivity.TYPE_OPEN_WATER_SWIM]):
            self._generate_swim_xml_data(el_activity)
        el_creator = xml_et.SubElement(el_activity, 'Creator')
        el_creator.set('xsi:type', 'Device_t')
        el_name = xml_et.SubElement(el_creator, 'Name')
        el_name.text = 'Huawei Fitness Tracking Device'
        el_unit_id = xml_et.SubElement(el_creator, 'UnitId')
        el_unit_id.text = '0000000000'
        el_product_id = xml_et.SubElement(el_creator, 'ProductID')
        el_product_id.text = '0000'
        el_version = xml_et.SubElement(el_creator, 'Version')
        el_version_major = xml_et.SubElement(el_version, 'VersionMajor')
        el_version_major.text = '0'
        el_version_minor = xml_et.SubElement(el_version, 'VersionMinor')
        el_version_minor.text = '0'
        el_build_major = xml_et.SubElement(el_version, 'BuildMajor')
        el_build_major.text = '0'
        el_build_minor = xml_et.SubElement(el_version, 'BuildMinor')
        el_build_minor.text = '0'
        el_author = xml_et.SubElement(training_center_database, 'Author')
        el_author.set('xsi:type', 'Application_t')
        el_name = xml_et.SubElement(el_author, 'Name')
        el_name.text = PROGRAM_NAME
        el_build = xml_et.SubElement(el_author, 'Build')
        el_version = xml_et.SubElement(el_build, 'Version')
        el_version_major = xml_et.SubElement(el_version, 'VersionMajor')
        el_version_major.text = PROGRAM_MAJOR_VERSION
        el_version_minor = xml_et.SubElement(el_version, 'VersionMinor')
        el_version_minor.text = PROGRAM_MINOR_VERSION
        el_build_major = xml_et.SubElement(el_version, 'BuildMajor')
        el_build_major.text = PROGRAM_MAJOR_BUILD
        el_build_minor = xml_et.SubElement(el_version, 'BuildMinor')
        el_build_minor.text = PROGRAM_MINOR_BUILD
        el_lang_id = xml_et.SubElement(el_author, 'LangID')
        el_lang_id.text = 'en'
        el_part_number = xml_et.SubElement(el_author, 'PartNumber')
        el_part_number.text = '000-00000-00'
    except Exception as e:
        logging.error('Error generating TCX XML content for activity <%s>\n%s', self.hi_activity.activity_id, e)
        raise Exception('Error generating TCX XML content for activity <%s>\n%s', self.hi_activity.activity_id, e)
    self.training_center_database = training_center_database
    return training_center_database
