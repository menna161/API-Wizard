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


def _initialize(self, date_time: datetime.datetime, header: List[str], block_names: List[str], conf: Tuple) -> None:
    'Initialize PhantomConfig.'
    (variables, values, comments, blocks) = (conf[0], conf[1], conf[2], conf[3])
    self.header = header
    self.datetime = date_time
    self.config = {var: ConfigVariable(var, val, comment, block) for (var, val, comment, block) in zip(variables, values, comments, blocks)}
