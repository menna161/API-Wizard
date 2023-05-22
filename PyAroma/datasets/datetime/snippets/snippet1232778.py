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


def _convert_timedelta_to_str(val: datetime.timedelta) -> str:
    'Convert datetime.timedelta to a string.\n\n    Parameters\n    ----------\n    val\n        The value as datetime.timedelta.\n\n    Returns\n    -------\n    str\n        The timedelta as a string like "HHH:MM".\n    '
    hhh = int((val.total_seconds() / 3600))
    mm = int(((val.total_seconds() - (3600 * hhh)) / 60))
    return f'{hhh:03}:{mm:02}'
