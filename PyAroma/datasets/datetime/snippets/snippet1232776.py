from __future__ import annotations
import datetime
import json
import math
import pathlib
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from .parsers import parse_dict_flat, parse_dict_nested, parse_json_file, parse_phantom_file, parse_toml_file
import tomlkit


def _serialize_datetime_for_json(val: Union[(datetime.datetime, datetime.timedelta)]) -> str:
    'Serialize datetime objects for JSON.\n\n    Parameters\n    ----------\n    val\n        The value as datetime.datetime or datetime.timedelta.\n\n    Returns\n    -------\n    str\n        The datetime as a string like "dd/mm/yyyy HH:MM:SS.f", or\n        timdelta as string like "HHH:MM".\n    '
    if isinstance(val, datetime.datetime):
        return _convert_datetime_to_str(val)
    elif isinstance(val, datetime.timedelta):
        return _convert_timedelta_to_str(val)
    else:
        raise ValueError('Cannot serialize object')
