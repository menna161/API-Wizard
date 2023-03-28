import traceback
from urllib.request import urlopen
import json
from time import sleep
import geomath
import math
from datetime import datetime
from configparser import ConfigParser
import os


def _parse_aircraft_data(self, a, time):
    alt = a.get('Alt', 0)
    dist = (- 1)
    az = 0
    el = 0
    if (('Lat' in a) and ('Long' in a)):
        rec_pos = (receiver_latitude, receiver_longitude)
        ac_pos = (a['Lat'], a['Long'])
        dist = geomath.distance(rec_pos, ac_pos)
        az = geomath.bearing(rec_pos, ac_pos)
        el = math.degrees(math.atan((alt / (dist * 5280))))
    speed = 0
    if ('Spd' in a):
        speed = geomath.knot2mph(a['Spd'])
    if ('PosTime' in a):
        last_seen_time = datetime.fromtimestamp((a['PosTime'] / 1000.0))
        seen = (time - last_seen_time).total_seconds()
    else:
        seen = 0
    ac_data = AirCraftData(a.get('Icao', None).upper(), a.get('Sqk', None), a.get('Call', None), a.get('Reg', None), a.get('Lat', None), a.get('Long', None), alt, a.get('Vsi', 0), a.get('Trak', None), speed, a.get('CMsgs', None), seen, a.get('Mlat', False), None, None, (10.0 * math.log10(((a.get('Sig', 0) / 255.0) + 1e-05))), dist, az, el, time)
    return ac_data
