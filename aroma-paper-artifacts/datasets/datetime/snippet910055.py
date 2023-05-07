import os
import copy
import collections
import datetime
import six
import warnings
import numpy as np
import FlowCal.plot


@property
def acquisition_start_time(self):
    '\n        Acquisition start time, as a python time or datetime object.\n\n        `acquisition_start_time` is taken from the $BTIM keyword parameter\n        in the TEXT segment of the FCS file. If date information is also\n        found, `acquisition_start_time` is a datetime object with the\n        acquisition date. If not, `acquisition_start_time` is a\n        datetime.time object. If no start time is found in the FCS file,\n        return None.\n\n        '
    return self._acquisition_start_time
