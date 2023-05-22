import datetime
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from tomlkit import loads


def parse_phantom_file(filepath: Union[(str, Path)]) -> Any:
    'Parse Phantom config file.\n\n    Parameters\n    ----------\n    filepath\n        The file name or path to the JSON file.\n\n    Returns\n    -------\n    date_time : datetime.datetime\n    header : list\n    block_names : list\n    (variables, values, comments, blocks) : Tuple[str, Any, str, str]\n    '
    with open(filepath, mode='r') as fp:
        variables = list()
        values = list()
        comments = list()
        header = list()
        blocks = list()
        block_names = list()
        _read_in_header = False
        for line in fp:
            if line.startswith('#'):
                if (not _read_in_header):
                    header.append(line.strip().split('# ')[1])
                else:
                    block_name = line.strip().split('# ')[1]
                    block_names.append(block_name)
            if ((not _read_in_header) and (line == '\n')):
                _read_in_header = True
            line = line.split('#', 1)[0].strip()
            if line:
                (line, comment) = line.split('!')
                comments.append(comment.strip())
                (variable, value) = line.split('=', 1)
                variables.append(variable.strip())
                value = value.strip()
                value = _convert_value_type_phantom(value)
                values.append(value)
                blocks.append(block_name)
    date_time = _get_datetime_from_header(header)
    return (date_time, header, block_names, (variables, values, comments, blocks))
