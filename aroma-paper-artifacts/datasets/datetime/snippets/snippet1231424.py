import logging
import socket
import sys
import threading
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
import structlog
from dateutil.tz import tzlocal


def add_local_timestamp(logger, method_name, event_dict):
    now = datetime.now(LOCAL_TZ)
    event_dict['@timestamp'] = now.isoformat(timespec='milliseconds')
    return event_dict
