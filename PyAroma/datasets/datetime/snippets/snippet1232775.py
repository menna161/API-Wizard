import datetime
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from tomlkit import loads


def _convert_value_type_phantom(value: str) -> Any:
    'Convert string from Phantom config to appropriate type.\n\n    Parameters\n    ----------\n    value\n        The value as a string.\n\n    Returns\n    -------\n    value\n        The value as appropriate type.\n    '
    float_regexes = ['\\d*\\.\\d*[Ee][-+]\\d*', '-*\\d*\\.\\d*']
    timedelta_regexes = ['\\d\\d\\d:\\d\\d']
    int_regexes = ['-*\\d+']
    if (value == 'T'):
        return True
    if (value == 'F'):
        return False
    for regex in float_regexes:
        if re.fullmatch(regex, value):
            return float(value)
    for regex in timedelta_regexes:
        if re.fullmatch(regex, value):
            (hours, minutes) = value.split(':')
            return datetime.timedelta(hours=int(hours), minutes=int(minutes))
    for regex in int_regexes:
        if re.fullmatch(regex, value):
            return int(value)
    return value
