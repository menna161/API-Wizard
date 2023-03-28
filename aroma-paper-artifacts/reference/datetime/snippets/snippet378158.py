import datetime
import gpio_pin
import inspect
import json
import logging
import math
import os
import psutil
import RPi.GPIO as gpio
import salt.loader
import threading
from common_util import abs_file_path, factory_rendering
from messaging import EventDrivenMessageProcessor, filter_out_unchanged
from threading_more import intercept_exit_signal, TimedEvent
from timeit import default_timer as timer
from lsm6dsl_conn import LSM6DSLConn
from mma8x5x_conn import MMA8X5XConn


@edmp.register_hook()
def dump_handler(duration=1, range=8, rate=12.5, decimals=4, timestamp=True, sound=True, interrupt_driven=True, file=None):
    "\n    Dumps raw XYZ readings to screen or file.\n\n    Optional arguments:\n      - duration (int): How many seconds to record data? Default value is '1'.\n      - file (str): Write data to a file with the given name.\n      - range (int): Maximum number of g-forces being measured. Default value is '8'.\n      - rate (float): How many Hz (samples per second)? Default value is '12.5'.\n      - decimals (int): How many decimals to calculate? Default value is '4'.\n      - timestamp (bool): Add timestamp to each sample? Default value is 'True'.\n      - sound (bool): Play sound when starting and stopping recording? Default value is 'True'.\n      - interrupt_driven (bool): Await hardware data ready signal before reading a sample? Default value is 'True'.\n    "
    if (duration > 300):
        raise ValueError('Maximum duration is 300 seconds')
    if (((duration * rate) > 100) and (file == None)):
        raise ValueError("Too much data to return - please adjust parameters 'duration' and 'rate' or instead specify a file to write to")
    file_path = (abs_file_path(file, '/opt/autopi/acc', ext='json') if (file != None) else None)
    if ((file_path != None) and os.path.isfile(file_path)):
        raise ValueError('File already exists: {:}'.format(file_path))
    ret = {'range': range, 'rate': rate, 'decimals': decimals}
    if interrupt_driven:
        ret['interrupt_timeouts'] = 0
    data = []
    orig_range = conn.range
    orig_rate = conn.rate
    try:
        if sound:
            __salt__['cmd.run']('aplay /opt/autopi/audio/sound/bleep.wav')
        conn.configure(range=range, rate=rate)
        interrupt_timeout = (2.0 / rate)
        start = timer()
        stop = (start + duration)
        while (timer() < stop):
            if interrupt_driven:
                if (not interrupt_event.wait(timeout=interrupt_timeout)):
                    ret['interrupt_timeouts'] += 1
                interrupt_event.clear()
            res = conn.xyz(decimals=decimals)
            if timestamp:
                res['_stamp'] = datetime.datetime.utcnow().isoformat()
            data.append(res)
        ret['duration'] = (timer() - start)
        ret['samples'] = len(data)
    finally:
        conn.configure(range=orig_range, rate=orig_rate)
        if sound:
            __salt__['cmd.run']('aplay /opt/autopi/audio/sound/beep.wav')
    if (file_path != None):
        __salt__['file.mkdir'](os.path.dirname(file_path))
        with open(file_path, 'w') as f:
            res = ret.copy()
            res['data'] = data
            json.dump(res, f, indent=4)
            ret['file'] = f.name
    else:
        ret['data'] = data
    return ret
