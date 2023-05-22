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


def _to_phantom_lines(self, block: str=None) -> List[str]:
    'Convert config to a list of lines in Phantom style.\n\n        Optional Parameters\n        -------------------\n        block\n            Only return the lines of the specified block.\n\n        Returns\n        -------\n        list\n            The config file as a list of lines.\n        '
    _length = 12
    only_block = None
    if (block is not None):
        only_block = block
    lines = list()
    if (only_block is None):
        if (self.header is not None):
            for header_line in self.header:
                lines.append((('# ' + header_line) + '\n'))
            lines.append('\n')
    for (block_name, block_contents) in self._dictionary_in_blocks().items():
        if ((only_block is not None) and (block_name != only_block)):
            continue
        if (block_name in ['__header__', '__datetime__']):
            pass
        else:
            lines.append((('# ' + block_name) + '\n'))
            for (var, val, comment) in block_contents:
                if isinstance(val, bool):
                    val_string = ('T'.rjust(_length) if val else 'F'.rjust(_length))
                elif isinstance(val, float):
                    val_string = _phantom_float_format(val, length=_length, justify='right')
                elif isinstance(val, int):
                    val_string = f'{val:>{_length}}'
                elif isinstance(val, str):
                    val_string = f'{val:>{_length}}'
                elif isinstance(val, datetime.timedelta):
                    hhh = int((val.total_seconds() / 3600))
                    mm = int(((val.total_seconds() - (3600 * hhh)) / 60))
                    val_string = f'{hhh:03}:{mm:02}'.rjust(_length)
                else:
                    raise ValueError('Cannot determine type')
                lines.append(((f'{var:>20} = ' + val_string) + f'''   ! {comment}
'''))
            lines.append('\n')
    return lines[:(- 1)]
