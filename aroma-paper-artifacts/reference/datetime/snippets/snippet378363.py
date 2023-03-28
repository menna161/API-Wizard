import datetime
import decimal
import logging
import nmea_util
import os
import pynmea2
from messaging import EventDrivenMessageClient, msg_pack as _msg_pack
from pynmea2 import nmea_utils


def gnss_assist_time(timestamp=datetime.datetime.utcnow(), operation=0, utc=True, force=False, uncertainty_ms=0):
    '\n    This command can be used to inject gpsOneXTRA time to GNSS engine. Before using it,\n    customers must enable gpsOneXTRA Assistance function via AT+QGPSXTRA=1 command.\n    After activating the function, the GNSS engine will ask for gpsOneXTRA time and\n    assistance data file. Before injecting gpsOneXTRA data file, gpsOneXTRA time must\n    be injected first via this command.\n    '
    return query('AT+QGPSXTRATIME={:d},"{:%Y/%m/%d,%H:%M:%S}",{:d},{:d},{:d}'.format(operation, timestamp, utc, force, uncertainty_ms))
