import json
import os
from sap.cf_logging.defaults import UNIX_EPOCH


def epoch_nano_second(datetime_):
    ' Returns the nanoseconds since epoch time '
    return ((int((datetime_ - UNIX_EPOCH).total_seconds()) * 1000000000) + (datetime_.microsecond * 1000))
