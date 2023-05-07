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


def write_toml(self, filename: Union[(str, Path)]) -> PhantomConfig:
    'Write config to TOML file.\n\n        Parameters\n        ----------\n        filename\n            The name of the TOML output file.\n        '
    import tomlkit
    document = tomlkit.document()
    if (self.header is not None):
        for line in self.header:
            document.add(tomlkit.comment(line))
        document.add(tomlkit.nl())
    d = self.to_dict()
    for (block_key, block_val) in d.items():
        block = tomlkit.table()
        if isinstance(block_val, dict):
            for (name, item) in block_val.items():
                (value, comment) = item
                if isinstance(value, datetime.timedelta):
                    value = _convert_timedelta_to_str(value)
                block.add(tomlkit.nl())
                if (comment is not None):
                    block.add(tomlkit.comment(comment))
                block.add(name, value)
            document.add(block_key, block)
    with open(filename, 'w') as fp:
        fp.write(tomlkit.dumps(document))
    return self
