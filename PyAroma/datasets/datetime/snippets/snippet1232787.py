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


def write_json(self, filename: Union[(str, Path)]) -> PhantomConfig:
    'Write config to JSON file.\n\n        Parameters\n        ----------\n        filename\n            The name of the JSON output file.\n        '
    with open(filename, mode='w') as fp:
        json.dump(self._dictionary_in_blocks(), fp, indent=4, sort_keys=False, default=_serialize_datetime_for_json)
    return self
