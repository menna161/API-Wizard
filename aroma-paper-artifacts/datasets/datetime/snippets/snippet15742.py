import json
import os
from sap.cf_logging.defaults import UNIX_EPOCH


def iso_time_format(datetime_):
    ' Returns ISO time formatted string '
    return ('%04d-%02d-%02dT%02d:%02d:%02d.%03dZ' % (datetime_.year, datetime_.month, datetime_.day, datetime_.hour, datetime_.minute, datetime_.second, int((datetime_.microsecond / 1000))))
