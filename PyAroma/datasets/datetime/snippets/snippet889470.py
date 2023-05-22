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


def _write_location(output, format, location, separator, first, last_location):
    'Writes the data for one location to output according to specified format'
    if ((format == 'json') or (format == 'js')):
        if (not first):
            output.write(',')
        if ('timestampMs' in location):
            item = {'timestampMs': location['timestampMs'], 'latitudeE7': location['latitudeE7'], 'longitudeE7': location['longitudeE7']}
        else:
            item = {'timestamp': location['timestamp'], 'latitudeE7': location['latitudeE7'], 'longitudeE7': location['longitudeE7']}
        output.write(json.dumps(item, separators=(',', ':')))
        return
    if ((format == 'jsonfull') or (format == 'jsfull')):
        if (not first):
            output.write(',')
        output.write(json.dumps(location, separators=(',', ':')))
        return
    if (format == 'csv'):
        output.write((separator.join([datetime.utcfromtimestamp((int(_get_timestampms(location)) / 1000)).strftime('%Y-%m-%d %H:%M:%S'), ('%.8f' % (location['latitudeE7'] / 10000000)), ('%.8f' % (location['longitudeE7'] / 10000000))]) + '\n'))
    if (format == 'csvfull'):
        output.write((separator.join([datetime.utcfromtimestamp((int(_get_timestampms(location)) / 1000)).strftime('%Y-%m-%d %H:%M:%S'), ('%.8f' % (location['latitudeE7'] / 10000000)), ('%.8f' % (location['longitudeE7'] / 10000000)), str(location.get('accuracy', '')), str(location.get('altitude', '')), str(location.get('verticalAccuracy', '')), str(location.get('velocity', '')), str(location.get('heading', ''))]) + '\n'))
    if (format == 'csvfullest'):
        output.write((separator.join([datetime.utcfromtimestamp((int(_get_timestampms(location)) / 1000)).strftime('%Y-%m-%d %H:%M:%S'), ('%.8f' % (location['latitudeE7'] / 10000000)), ('%.8f' % (location['longitudeE7'] / 10000000)), str(location.get('accuracy', '')), str(location.get('altitude', '')), str(location.get('verticalAccuracy', '')), str(location.get('velocity', '')), str(location.get('heading', ''))]) + separator))
        if ('activity' in location):
            a = _read_activity(location['activity'])
            output.write((separator.join([str(len(a)), str(a.get('UNKNOWN', '')), str(a.get('STILL', '')), str(a.get('TILTING', '')), str(a.get('ON_FOOT', '')), str(a.get('WALKING', '')), str(a.get('RUNNING', '')), str(a.get('IN_VEHICLE', '')), str(a.get('ON_BICYCLE', '')), str(a.get('IN_ROAD_VEHICLE', '')), str(a.get('IN_RAIL_VEHICLE', '')), str(a.get('IN_TWO_WHEELER_VEHICLE', '')), str(a.get('IN_FOUR_WHEELER_VEHICLE', ''))]) + '\n'))
        else:
            output.write((('0' + separator.join(([''] * 13))) + '\n'))
    if (format == 'kml'):
        output.write('    <Placemark>\n')
        output.write('      <TimeStamp><when>')
        time = datetime.utcfromtimestamp((int(_get_timestampms(location)) / 1000))
        output.write(time.strftime('%Y-%m-%dT%H:%M:%SZ'))
        output.write('</when></TimeStamp>\n')
        if (('accuracy' in location) or ('speed' in location) or ('altitude' in location)):
            output.write('      <ExtendedData>\n')
            if ('accuracy' in location):
                output.write('        <Data name="accuracy">\n')
                output.write(('          <value>%d</value>\n' % location['accuracy']))
                output.write('        </Data>\n')
            if ('speed' in location):
                output.write('        <Data name="speed">\n')
                output.write(('          <value>%d</value>\n' % location['speed']))
                output.write('        </Data>\n')
            if ('altitude' in location):
                output.write('        <Data name="altitude">\n')
                output.write(('          <value>%d</value>\n' % location['altitude']))
                output.write('        </Data>\n')
            output.write('      </ExtendedData>\n')
        output.write(('      <Point><coordinates>%s,%s</coordinates></Point>\n' % ((location['longitudeE7'] / 10000000), (location['latitudeE7'] / 10000000))))
        output.write('    </Placemark>\n')
    if (format == 'gpx'):
        output.write(('  <wpt lat="%s" lon="%s">\n' % ((location['latitudeE7'] / 10000000), (location['longitudeE7'] / 10000000))))
        if ('altitude' in location):
            output.write(('    <ele>%d</ele>\n' % location['altitude']))
        time = datetime.utcfromtimestamp((int(_get_timestampms(location)) / 1000))
        output.write(('    <time>%s</time>\n' % time.strftime('%Y-%m-%dT%H:%M:%SZ')))
        output.write(('    <desc>%s' % time.strftime('%Y-%m-%d %H:%M:%S')))
        if (('accuracy' in location) or ('speed' in location)):
            output.write(' (')
            if ('accuracy' in location):
                output.write(('Accuracy: %d' % location['accuracy']))
            if (('accuracy' in location) and ('speed' in location)):
                output.write(', ')
            if ('speed' in location):
                output.write(('Speed:%d' % location['speed']))
            output.write(')')
        output.write('</desc>\n')
        output.write('  </wpt>\n')
    if (format == 'gpxtracks'):
        if first:
            output.write('  <trk>\n')
            output.write('    <trkseg>\n')
        if last_location:
            timedelta = abs((((int(_get_timestampms(location)) - int(_get_timestampms(last_location))) / 1000) / 60))
            distancedelta = _distance((location['latitudeE7'] / 10000000), (location['longitudeE7'] / 10000000), (last_location['latitudeE7'] / 10000000), (last_location['longitudeE7'] / 10000000))
            if ((timedelta > 10) or (distancedelta > 40)):
                output.write('    </trkseg>\n')
                output.write('  </trk>\n')
                output.write('  <trk>\n')
                output.write('    <trkseg>\n')
        output.write(('      <trkpt lat="%s" lon="%s">\n' % ((location['latitudeE7'] / 10000000), (location['longitudeE7'] / 10000000))))
        if ('altitude' in location):
            output.write(('        <ele>%d</ele>\n' % location['altitude']))
        time = datetime.utcfromtimestamp((int(_get_timestampms(location)) / 1000))
        output.write(('        <time>%s</time>\n' % time.strftime('%Y-%m-%dT%H:%M:%SZ')))
        if (('accuracy' in location) or ('speed' in location)):
            output.write('        <desc>\n')
            if ('accuracy' in location):
                output.write(('          Accuracy: %d\n' % location['accuracy']))
            if ('speed' in location):
                output.write(('          Speed:%d\n' % location['speed']))
            output.write('        </desc>\n')
        output.write('      </trkpt>\n')
