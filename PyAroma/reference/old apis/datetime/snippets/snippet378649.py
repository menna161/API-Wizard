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


def spawn_subprocess():
    conn.ensure_protocol(protocol, baudrate=baudrate, verify=verify)
    if monitor_filtering:
        _ensure_filtering(monitor_filtering)
    conn.interface().set_can_monitor_mode(monitor_mode)
    conn.interface().set_can_auto_format(can_auto_format)
    if serial_baudrate:
        conn.change_baudrate(serial_baudrate)
    protocol_folder = os.path.join(folder, 'protocol_{:}'.format(conn.cached_protocol.ID))
    if (not os.path.exists(protocol_folder)):
        os.makedirs(protocol_folder)
    serial = conn.serial()
    cmd = ['/usr/bin/stn-dump', '-d', serial.portstr, '-b', str(serial.baudrate), '-c', ('STM' if monitor_filtering else 'STMA'), '-t', str((read_timeout * 10)), '-o', os.path.join(protocol_folder, '{:%Y%m%d%H%M}.log'.format(datetime.datetime.utcnow())), '-q']
    log.info('Spawning export subprocess by running command: {:}'.format(' '.join(cmd)))
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=(lambda : os.nice(process_nice)))
