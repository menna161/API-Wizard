import os
import copy
import collections
import datetime
import six
import warnings
import numpy as np
import FlowCal.plot


@staticmethod
def _parse_date_string(date_str):
    "\n        Get a datetime.date object from a string date representation.\n\n        The FCS standard includes an optional keyword parameter $DATE in\n        which the acquistion date is stored. In FCS 2.0, the date is saved\n        as 'dd-mmm-yy', whereas in FCS 3.0 and 3.1 the date is saved as\n        'dd-mmm-yyyy'.\n\n        This function attempts to parse these formats, along with a couple\n        of nonstandard ones, using the datetime module.\n\n        Parameters:\n        -----------\n        date_str : str, or None\n            String representation of date, or None.\n\n        Returns:\n        --------\n        t : datetime.datetime, or None\n            Date parsed from `date_str`. If parsing was not possible,\n            return None. If `date_str` is None, return None\n\n        "
    if (date_str is None):
        return None
    try:
        return datetime.datetime.strptime(date_str, '%d-%b-%y')
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(date_str, '%d-%b-%Y')
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(date_str, '%y-%b-%d')
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(date_str, '%Y-%b-%d')
    except ValueError:
        pass
    return None
