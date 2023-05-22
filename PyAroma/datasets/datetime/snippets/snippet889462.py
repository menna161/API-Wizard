from __future__ import division
import sys
import json
import math
from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime
from datetime import timedelta
from dateutil.parser import isoparse
from dateutil.tz import UTC
import ijson
from shapely.geometry import Point, Polygon


def _valid_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise ArgumentTypeError(msg)
