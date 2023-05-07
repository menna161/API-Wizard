import os
import copy
import collections
import datetime
import six
import warnings
import numpy as np
import FlowCal.plot


@property
def acquisition_end_time(self):
    '\n        Acquisition end time, as a python time or datetime object.\n\n        `acquisition_end_time` is taken from the $ETIM keyword parameter in\n        the TEXT segment of the FCS file. If date information is also\n        found, `acquisition_end_time` is a datetime object with the\n        acquisition date. If not, `acquisition_end_time` is a datetime.time\n        object. If no end time is found in the FCS file, return None.\n\n        '
    return self._acquisition_end_time
