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


def convert(locations, output, format='kml', js_variable='locationJsonData', separator=',', start_date=None, end_date=None, accuracy=None, polygon=None, chronological=False):
    'Converts the provided locations to the specified format\n\n    Parameters\n    ----------\n\n    locations : Iterable\n        list or other Iterable of locations from Google Takeout JSON file\n\n    output: File or StringIO or similar\n        All output will be written to this buffer\n\n    format: str\n        Format to convert to\n        Can be one of "kml", "json", "js", "jsonfull", "jsfull", "csv", "csvfull", "csvfullest", "gpx", "gpxtracks"\n        See README.md for details about those formats\n\n    js_variable: str\n        Variable name to be used for js output\n\n    separator: str\n        What separator to use for the csv formats\n\n    start_date: datetime\n        Locations before this date will be ignored\n\n    end_date: datetime\n        Locations after this date will be ignored\n\n    accuracy: int\n        Locations with a higher accuracy value (i.e. worse accuracy) will be ignored\n\n    polygon: shapely.Polygon\n        All locations outside of the Polygon will be ignored\n\n    chronological: bool\n        Whether to sort all timestamps in chronological order (required for gpxtracks)\n        This might be uncessary since recent Takeout data seems properly sorted already.\n    '
    if chronological:
        locations = sorted(locations, key=_get_timestampms)
    _write_header(output, format, js_variable, separator)
    first = True
    last_loc = None
    added = 0
    print('Progress:')
    for item in locations:
        if (('longitudeE7' not in item) or ('latitudeE7' not in item) or (('timestampMs' not in item) and ('timestamp' not in item))):
            continue
        time = datetime.utcfromtimestamp((int(_get_timestampms(item)) / 1000))
        print(('\r%s / Locations written: %s' % (time.strftime('%Y-%m-%d %H:%M'), added)), end='')
        if ((accuracy is not None) and ('accuracy' in item) and (item['accuracy'] > accuracy)):
            continue
        if ((start_date is not None) and (start_date > time)):
            continue
        if ((end_date is not None) and (end_date < time)):
            if chronological:
                break
            continue
        if (polygon and (not _check_point(polygon, item['latitudeE7'], item['longitudeE7']))):
            continue
        if (item['latitudeE7'] > 1800000000):
            item['latitudeE7'] = (item['latitudeE7'] - 4294967296)
        if (item['longitudeE7'] > 1800000000):
            item['longitudeE7'] = (item['longitudeE7'] - 4294967296)
        _write_location(output, format, item, separator, first, last_loc)
        if first:
            first = False
        last_loc = item
        added = (added + 1)
    _write_footer(output, format)
    print('')
