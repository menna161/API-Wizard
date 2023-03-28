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
def export_handler(run=None, folder=None, wait_timeout=0, monitor_filtering=False, monitor_mode=0, can_auto_format=False, read_timeout=1, serial_baudrate=None, process_nice=(- 2), protocol=None, baudrate=None, verify=False):
    "\n    Fast export of all messages on a bus to a log file.\n\n    Optional arguments:\n      - run (bool): Specify if subprocess should be running or not. If not defined the current state will be queried.\n      - folder (str): Custom folder to place export log files.\n      - wait_timeout (int): Maximum time in seconds to wait for subprocess to complete. Default value is '0'.\n      - monitor_filtering (bool): Use filters while monitoring or monitor all messages? Default value is 'False'. It is possible to specify 'can' or 'j1939' (PGN) in order to add filters based on the messages found in a CAN database file (.dbc).\n      - monitor_mode (int): The STN monitor mode. Default is '0'.\n      - can_auto_format (bool): Apply automatic formatting of messages? Default value is 'False'.\n      - read_timeout (int): How long time in seconds should the subprocess wait for data on the serial port? Default value is '1'.\n      - serial_baudrate (int): Specify a custom baud rate to use for the serial connection to the STN.\n      - process_nice (int): Process nice value that controls the priority of the subprocess. Default value is '-2'.\n      - protocol (str): ID of specific protocol to be used to receive the data. If none is specifed the current protocol will be used.\n      - baudrate (int): Specific protocol baudrate to be used. If none is specifed the current baudrate will be used.\n      - verify (bool): Verify that OBD-II communication is possible with the desired protocol? Default value is 'False'.\n    "
    ret = {}
    ctx = context.setdefault('export', {})
    folder = (folder or os.path.join(home_dir, 'export'))
    spawn_count = 0

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
    global export_subprocess
    if ((export_subprocess == None) and run):
        export_subprocess = spawn_subprocess()
        spawn_count += 1
        if (wait_timeout < (read_timeout + 1)):
            wait_timeout = (read_timeout + 1)
    if (export_subprocess != None):
        return_code = export_subprocess.poll()
        for i in range(0, (wait_timeout * 10)):
            return_code = export_subprocess.poll()
            if (return_code != None):
                break
            if (wait_timeout > 0):
                time.sleep(0.1)
        is_running = (return_code == None)
        ctx['timestamp'] = datetime.datetime.utcnow().isoformat()
        if is_running:
            if (run != None):
                if run:
                    log.info('Export subprocess is already running')
                else:
                    log.info('Sending interrupt signal to export subprocess')
                    export_subprocess.send_signal(signal.SIGINT)
                    is_running = False
        if (not is_running):
            try:
                (stdout, stderr) = export_subprocess.communicate()
                if stdout:
                    ret['lines'] = stdout.split('\n')
                    log.warning('Output received from export subprocess: {:}'.format(ret['lines']))
                if stderr:
                    ret['errors'] = stderr.split('\n')
                    log.error('Error(s) received from export subprocess: {:}'.format(ret['errors']))
                return_code = export_subprocess.returncode
            finally:
                export_subprocess = None
        if is_running:
            ctx['state'] = 'running'
        elif (return_code == 0):
            ctx['state'] = 'completed'
        else:
            ctx['state'] = 'failed'
            ctx['return_code'] = return_code
            log.error('Export subprocess failed with return code {:}'.format(return_code))
    else:
        ctx['state'] = 'stopped'
    ret['state'] = ctx['state']
    return ret
