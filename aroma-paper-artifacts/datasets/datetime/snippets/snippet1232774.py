import datetime
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from tomlkit import loads


def _get_datetime_from_header(header: List[str]) -> Optional[datetime.datetime]:
    'Get datetime from Phantom timestamp in header.\n\n    Phantom timestamp is like dd/mm/yyyy hh:mm:s.ms\n\n    Parameters\n    ----------\n    header\n        The header as a list of strings.\n\n    Returns\n    -------\n    datetime.datetime\n        The datetime of the config.\n    '
    date_time = None
    for line in header:
        if (date_time is not None):
            break
        matches = re.findall('\\d{2}/\\d{2}/\\d{4} \\d{2}:\\d{2}:\\d{2}.\\d+', line)
        if (len(matches) == 0):
            continue
        elif (len(matches) == 1):
            date_time = datetime.datetime.strptime(matches[0], '%d/%m/%Y %H:%M:%S.%f')
        else:
            raise ValueError('Too many date time values in line')
    return date_time
