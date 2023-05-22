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


def _to_dict_nested(self, only_values: bool=False) -> Dict[(str, Any)]:
    "Convert config to a nested dictionary.\n\n        Parameters\n        ----------\n        only_values\n            If True, keys are names, items are values.\n            If False, keys are names, items are tuples like\n                (val, comment, block).\n\n        Returns\n        -------\n        dict\n            The config file as a dictionary, like\n                {'block': 'variable': (value, comment), ...}.\n            or, if only_values is True, like\n                {'block': 'variable': value, ...}.\n        "
    nested_dict: Dict[(str, Any)] = dict()
    for block in self.blocks:
        names = [conf.name for conf in self.config.values() if (conf.block == block)]
        values = [conf.value for conf in self.config.values() if (conf.block == block)]
        comments = [conf.comment for conf in self.config.values() if (conf.block == block)]
        if only_values:
            nested_dict[block] = {name: value for (name, value) in zip(names, values)}
        else:
            nested_dict[block] = {name: (value, comment) for (name, value, comment) in zip(names, values, comments)}
    if (self.header is not None):
        nested_dict['__header__'] = self.header
    if (self.datetime is not None):
        nested_dict['__datetime__'] = self.datetime
    return nested_dict
