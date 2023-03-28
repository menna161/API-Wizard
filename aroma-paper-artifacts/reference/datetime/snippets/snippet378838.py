import datetime
import logging
import pynmea2
import salt.loader
from messaging import EventDrivenMessageProcessor, extract_error_from
from salt_more import SuperiorCommandExecutionError
from serial_conn import SerialConn
from threading_more import intercept_exit_signal


@edmp.register_hook()
def nmea0183_readout_to_position_converter(result):
    '\n    Converts NMEA0183 sentences result into position type.\n    '
    ret = {'_type': 'pos', '_stamp': datetime.datetime.utcnow().isoformat()}
    if (not ('gga' in result)):
        log.warn('No GGA sentence found in result')
    elif (result['gga'].gps_qual > 0):
        ret['utc'] = result['gga'].timestamp.isoformat()
        ret['loc'] = {'lat': result['gga'].latitude, 'lon': result['gga'].longitude}
        ret['alt'] = float(result['gga'].altitude)
        ret['nsat'] = int(result['gga'].num_sats)
    if ('vtg' in result):
        ret['sog'] = result['vtg'].spd_over_grnd_kmph
        ret['cog'] = 0
    return ret
