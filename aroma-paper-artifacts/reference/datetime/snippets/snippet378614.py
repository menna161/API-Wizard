import collections
import datetime
import logging
import obd
import obd.utils
import time
from binascii import unhexlify
from obd.interfaces import STN11XX
from obd.utils import format_frame, parse_frame
from retrying import retry


def _enrich_monitor_entry(self, res):
    ret = {'_stamp': datetime.datetime.utcnow().isoformat()}
    val = res.decode().rstrip()
    if (val in self._obd.interface.ERRORS):
        ret['error'] = self._obd.interface.ERRORS[val]
    else:
        ret['value'] = val
    return ret
