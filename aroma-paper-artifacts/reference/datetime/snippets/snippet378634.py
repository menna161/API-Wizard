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


@edmp.register_hook(synchronize=False)
def import_handler(folder=None, limit=5000, idle_sleep=0, cleanup_grace=60, process_nice=0, type='raw'):
    "\n    Fast import of exported log files containing messages from a bus.\n\n    Optional arguments:\n      - folder (str): Custom folder to import log files from.\n      - limit (int): The maximum number of lines/messages to read each time. Default value is '5000'.\n      - idle_sleep (int): Pause in seconds if there is no lines/messages to import. Default value is '0'.\n      - cleanup_grace (int): Grace period in seconds before a fully imported log file is deleted. Default value is '60'.\n      - process_nice (int): Process nice value that controls the priority of the service. Default value is '0'.\n      - type (str): Specify a name of the type of the result. Default is 'raw'.\n    "
    ret = {'_type': type, 'values': []}
    folder = (folder or os.path.join(home_dir, 'export', ('protocol_{:}'.format(conn.cached_protocol.ID) if conn.cached_protocol else '.')))
    if (not os.path.isdir(folder)):
        raise Warning("Folder '{:}' does not exist".format(folder))
    match = re.search('protocol_(?P<id>[0-9A]{1,2})', folder)
    if match:
        ret['protocol'] = match.group('id')
    if ((process_nice != None) and (process_nice != psutil.Process(os.getpid()).nice())):
        psutil.Process(os.getpid()).nice(process_nice)
    with open(os.path.join(folder, '.import'), ('r+' if os.path.isfile(os.path.join(folder, '.import')) else 'w+')) as metadata_file:
        metadata = {}
        if (os.path.getsize(metadata_file.name) > 0):
            try:
                metadata = json.load(metadata_file)
                if log.isEnabledFor(logging.DEBUG):
                    log.debug("Loaded import metadata from JSON file '{:}': {:}".format(metadata_file.name, metadata))
            except:
                metadata_file.seek(0)
                log.exception("Failed to load import metadata from JSON file '{:}': {:}".format(metadata_file.name, metadata_file.read()))
                log.warning("Skipped any progress that was stored in the invalid import metadata JSON file '{:}'".format(metadata_file.name))
        try:
            start = timer()
            count = 0
            files = [f for f in os.listdir(folder) if (os.path.isfile(os.path.join(folder, f)) and f.endswith('.log'))]
            for filename in [f for f in metadata.keys() if (not (f in files))]:
                metadata.pop(filename)
                log.info("Removed unaccompanied file entry '{:}' from import metadata".format(filename))
            for filename in sorted(files):
                metadata.setdefault(filename, {})
                offset = metadata[filename].get('offset', 0)
                size = metadata[filename].get('size', offset)
                if (size < os.path.getsize(os.path.join(folder, filename))):
                    if (count >= limit):
                        continue
                    with open(os.path.join(folder, filename), 'r') as file:
                        if (offset > 0):
                            file.seek(offset)
                            log.info("File '{:}' is partially imported - continuing from offset {:}".format(file.name, offset))
                        line = file.readline()
                        while line:
                            if (line[(- 1)] != '\n'):
                                log.info('Skipping incomplete line {:}'.format(repr(line)))
                                size = (offset + len(line))
                                break
                            count += 1
                            offset += len(line)
                            try:
                                parts = line.split(' ', 1)
                                ret['values'].append({'_stamp': datetime.datetime.fromtimestamp(float(parts[0])).isoformat(), 'value': parts[1].rstrip()})
                            except:
                                log.exception('Failed to import line {:}: {:}'.format(count, repr(line)))
                            if (count >= limit):
                                break
                            line = file.readline()
                        metadata[filename]['offset'] = offset
                        metadata[filename]['size'] = (size if (size > offset) else offset)
                        metadata[filename]['timestamp'] = datetime.datetime.utcnow().isoformat()
                else:
                    if log.isEnabledFor(logging.DEBUG):
                        log.debug("File '{:}' is already fully imported".format(os.path.join(folder, filename)))
                    if (cleanup_grace > 0):
                        try:
                            if ('timestamp' in metadata[filename]):
                                delta = (datetime.datetime.utcnow() - fromisoformat(metadata[filename]['timestamp']))
                                if (delta.total_seconds() < cleanup_grace):
                                    continue
                            os.remove(os.path.join(folder, filename))
                            metadata.pop(filename)
                            log.info("Cleaned up imported file '{:}'".format(os.path.join(folder, filename)))
                        except:
                            log.exception("Failed to cleanup imported file '{:}'".format(os.path.join(folder, filename)))
        finally:
            if log.isEnabledFor(logging.DEBUG):
                log.debug("Saving import metadata to JSON file '{:}': {:}".format(metadata_file.name, metadata))
            metadata_file.seek(0)
            metadata_file.truncate()
            json.dump(metadata, metadata_file, indent=4, sort_keys=True)
            metadata_file.flush()
        if (count > 0):
            log.info('Imported {:} line(s) in {:}'.format(count, (timer() - start)))
            if (count < limit):
                log.info('Did not import maximum data possible - sleeping for {} second(s)'.format(idle_sleep))
                time.sleep(idle_sleep)
        else:
            if (idle_sleep > 0):
                log.info('No data to import - sleeping for {:} second(s)'.format(idle_sleep))
                time.sleep(idle_sleep)
            raise Warning('No data to import')
    return ret
