from __future__ import division
import battery_util
import ConfigParser
import cProfile as profile
import datetime
import _strptime
import elm327_proxy
import io
import json
import logging
import math
import obd
import os
import psutil
import re
import RPi.GPIO as gpio
import salt.loader
import signal
import subprocess
import time
from collections import OrderedDict
from common_util import abs_file_path, add_rotating_file_handler_to, factory_rendering, fromisoformat
from obd.utils import OBDError
from obd_conn import OBDConn, decode_can_frame_for, FILTER_TYPE_CAN_PASS, FILTER_TYPE_J1939_PGN
from messaging import EventDrivenMessageProcessor, extract_error_from, filter_out_unchanged
from threading_more import intercept_exit_signal
from timeit import default_timer as timer
import cantools
import cantools


@edmp.register_hook()
def dump_handler(duration=2, monitor_mode=0, filtering=False, auto_format=False, raw_response=False, format_response=True, protocol=None, baudrate=None, verify=False, file=None, description=None):
    "\n    Dumps all messages from bus to screen or file.\n\n    Optional arguments:\n      - duration (int): How many seconds to record data? Default value is '2' seconds.\n      - file (str): Write data to a file with the given name.\n      - description (str): Additional description to the file.\n      - filtering (bool): Use filters while monitoring or monitor all messages? Default value is 'False'. It is possible to specify 'can' or 'j1939' (PGN) in order to add filters based on the messages found in a CAN database file (.dbc).\n      - protocol (str): ID of specific protocol to be used to receive the data. If none is specifed the current protocol will be used.\n      - baudrate (int): Specific protocol baudrate to be used. If none is specifed the current baudrate will be used.\n      - verify (bool): Verify that OBD-II communication is possible with the desired protocol? Default value is 'False'.\n      - raw_response (bool): Get raw response without any validation nor parsing? Default value is 'False'.\n      - format_response (bool): Format response messages by separating header and data with a hash sign? Default value is 'True'.\n    "
    ret = {}
    conn.ensure_protocol(protocol, baudrate=baudrate, verify=verify)
    if filtering:
        _ensure_filtering(filtering)
    __salt__['cmd.run']('aplay /opt/autopi/audio/sound/bleep.wav')
    try:
        res = conn.monitor(duration=duration, mode=monitor_mode, filtering=filtering, auto_format=auto_format, raw_response=raw_response, format_response=format_response)
    finally:
        __salt__['cmd.run']('aplay /opt/autopi/audio/sound/beep.wav')
    if (file != None):
        path = abs_file_path(file, home_dir)
        __salt__['file.mkdir'](os.path.dirname(path))
        protocol = conn.protocol(verify=verify)
        config_parser = ConfigParser.RawConfigParser(allow_no_value=True)
        config_parser.add_section('header')
        config_parser.set('header', 'timestamp', datetime.datetime.utcnow().isoformat())
        config_parser.set('header', 'duration', duration)
        config_parser.set('header', 'protocol', protocol['id'])
        config_parser.set('header', 'baudrate', protocol['baudrate'])
        config_parser.set('header', 'count', len(res))
        if description:
            config_parser.set('header', 'description', description)
        config_parser.add_section('data')
        for line in res:
            config_parser.set('data', line)
        with open(path, 'w') as f:
            config_parser.write(f)
            ret['file'] = f.name
    else:
        ret['data'] = res
    return ret
