import os
import copy
import collections
import datetime
import six
import warnings
import numpy as np
import FlowCal.plot


@staticmethod
def _parse_time_string(time_str):
    "\n        Get a datetime.time object from a string time representation.\n\n        The start and end of acquisition are stored in the optional keyword\n        parameters $BTIM and $ETIM. The following formats are used\n        according to the FCS standard:\n            - FCS 2.0: 'hh:mm:ss'\n            - FCS 3.0: 'hh:mm:ss[:tt]', where 'tt' is optional, and\n              represents fractional seconds in 1/60ths.\n            - FCS 3.1: 'hh:mm:ss[.cc]', where 'cc' is optional, and\n              represents fractional seconds in 1/100ths.\n        This function attempts to transform these formats to\n        'hh:mm:ss:ffffff', where 'ffffff' is in microseconds, and then\n        parse it using the datetime module.\n\n        Parameters:\n        -----------\n        time_str : str, or None\n            String representation of time, or None.\n\n        Returns:\n        --------\n        t : datetime.time, or None\n            Time parsed from `time_str`. If parsing was not possible,\n            return None. If `time_str` is None, return None\n\n        "
    if (time_str is None):
        return None
    time_l = time_str.split(':')
    if (len(time_l) == 3):
        if ('.' in time_l[2]):
            time_str = time_str.replace('.', ':')
        else:
            time_str = (time_str + ':0')
        try:
            t = datetime.datetime.strptime(time_str, '%H:%M:%S:%f').time()
        except:
            t = None
    elif (len(time_l) == 4):
        time_l[3] = '{:06d}'.format(int(((float(time_l[3]) * 1000000.0) / 60)))
        time_str = ':'.join(time_l)
        try:
            t = datetime.datetime.strptime(time_str, '%H:%M:%S:%f').time()
        except:
            t = None
    else:
        t = None
    return t
