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


def _add_segment_stop(self, segment_stop: datetime, segment_distance: int=(- 1)):
    logging.debug('Adding segment stop at %s', segment_stop)
    if (not self._current_segment):
        logging.error('Request to stop segment at %s when there is no current segment active', segment_stop)
        return
    self._current_segment['stop'] = segment_stop
    self._current_segment['duration'] = int((segment_stop - self._current_segment['start']).total_seconds())
    if (not (segment_distance == (- 1))):
        self._current_segment['distance'] = segment_distance
    self._current_segment = None
