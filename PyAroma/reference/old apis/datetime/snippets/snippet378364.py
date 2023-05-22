import datetime
import decimal
import logging
import nmea_util
import os
import pynmea2
from messaging import EventDrivenMessageClient, msg_pack as _msg_pack
from pynmea2 import nmea_utils


def gnss_assist_data(filename=None, storage='ufs'):
    '\n    Query the status or specify gpsOneXTRA data file.\n    '
    if filename:
        res = query('AT+QGPSXTRADATA="{:s}"'.format(_qf_name(filename, storage)), cooldown_delay=1)
        return res
    res = query('AT+QGPSXTRADATA?')
    if ('data' in res):
        row = _parse_dict(res.pop('data'))['+QGPSXTRADATA'].split(',', 1)
        dur_mins = int(row[0])
        start_dt = datetime.datetime.strptime(row[1].strip('"'), '%Y/%m/%d,%H:%M:%S')
        end_dt = (start_dt + datetime.timedelta(minutes=dur_mins))
        exp_mins = ((end_dt - datetime.datetime.now()).total_seconds() / 60)
        res.update({'valid_duration_mins': dur_mins, 'valid_start': start_dt.isoformat(), 'valid_end': end_dt.isoformat(), 'expire_mins': exp_mins, 'valid_mins': (dur_mins - exp_mins)})
    return res
