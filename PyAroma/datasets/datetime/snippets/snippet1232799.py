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


def _dictionary_in_blocks(self) -> Dict:
    'Return dictionary of config values with blocks as keys.'
    block_dict: Dict = dict()
    for block in self.blocks:
        block_dict[block] = list()
        names = [conf.name for conf in self.config.values() if (conf.block == block)]
        values = [conf.value for conf in self.config.values() if (conf.block == block)]
        comments = [conf.comment for conf in self.config.values() if (conf.block == block)]
        for (name, value, comment) in zip(names, values, comments):
            block_dict[block].append([name, value, comment])
    if (self.header is not None):
        block_dict['__header__'] = self.header
    if (self.datetime is not None):
        block_dict['__datetime__'] = self.datetime
    return block_dict
