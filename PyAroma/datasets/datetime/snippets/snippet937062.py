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


def _add_segment_start(self, segment_start: datetime):
    if self._current_segment:
        logging.error('Request to start segment at %s when there is already a current segment active', segment_start)
        return
    logging.debug('Adding segment start at %s', segment_start)
    self._current_segment = {'start': segment_start, 'stop': None}
    if (not self._segment_list):
        self._segment_list = []
    self._segment_list.append(self._current_segment)
    if (not self.start):
        self.start = segment_start
