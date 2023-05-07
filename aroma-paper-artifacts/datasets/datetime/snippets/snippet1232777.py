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


def _convert_datetime_to_str(val: datetime.datetime) -> str:
    'Convert datetime.datetime to a string.\n\n    Parameters\n    ----------\n    val\n        The value as datetime.datetime.\n\n    Returns\n    -------\n    str\n        The datetime as a string like "dd/mm/yyyy HH:MM:SS.f".\n    '
    return datetime.datetime.strftime(val, '%d/%m/%Y %H:%M:%S.%f')
